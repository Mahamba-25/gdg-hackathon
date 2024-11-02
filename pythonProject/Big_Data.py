import torch
from transformers import RobertaForQuestionAnswering, RobertaTokenizer, Trainer, TrainingArguments
from datasets import load_dataset, load_metric

# Load model and tokenizer
model_name = "nur-dev/roberta-kaz-large"
model = RobertaForQuestionAnswering.from_pretrained(model_name)
tokenizer = RobertaTokenizer.from_pretrained(model_name)

# Correct loading dataset without errors
dataset = load_dataset("issai/kazqad")


# Preprocess function
def preprocess_data(examples):
    inputs = examples["question"]
    contexts = examples["context"]
    answers = examples["answers"]

    # Tokenize inputs and contexts
    tokenized_examples = tokenizer(
        inputs,
        contexts,
        truncation=True,
        padding="longest",  # Adjusted for efficiency
        max_length=384
    )

    # Calculate answer start and end positions in tokenized text
    start_positions = []
    end_positions = []
    for i, answer in enumerate(answers):
        answer_text = answer["text"][0]
        start_char = answer["answer_start"][0]

        # Find the start position within tokenized context
        token_start_index = tokenized_examples["input_ids"][i].index(tokenizer.sep_token_id) + 1
        tokenized_answer = tokenizer(answer_text, add_special_tokens=False)["input_ids"]
        answer_start = tokenized_examples["input_ids"][i].index(tokenized_answer[0], token_start_index)
        answer_end = answer_start + len(tokenized_answer) - 1

        start_positions.append(answer_start)
        end_positions.append(answer_end)

    tokenized_examples["start_positions"] = start_positions
    tokenized_examples["end_positions"] = end_positions
    return tokenized_examples


# Apply preprocessing to dataset
tokenized_dataset = dataset.map(preprocess_data, batched=True)

# Define Training Arguments
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=3e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
    gradient_accumulation_steps=2,
    warmup_steps=500,
    gradient_checkpointing=True
)

# Define compute_metrics function
metric_f1 = load_metric("f1")
metric_em = load_metric("exact_match")


def compute_metrics(eval_preds):
    start_preds, end_preds = eval_preds.predictions
    start_labels, end_labels = eval_preds.label_ids
    f1 = metric_f1.compute(predictions=start_preds, references=start_labels)["f1"]
    em = metric_em.compute(predictions=start_preds, references=start_labels)["exact_match"]
    return {
        "f1": f1,
        "exact_match": em,
    }


# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["validation"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)

# Train the model
trainer.train()

# Evaluate the model on the test set
metrics = trainer.evaluate(tokenized_dataset["test"])
print(metrics)

# Save the fine-tuned model and tokenizer
model.save_pretrained("./fine_tuned_roberta_kaz_large")
tokenizer.save_pretrained("./fine_tuned_roberta_kaz_large")
