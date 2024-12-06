import torch
import pandas as pd
from datasets import Dataset
from transformers import BertForSequenceClassification, AutoTokenizer, Trainer, TrainingArguments, DefaultDataCollator
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

from airosentris.trainer.BaseTrainer import BaseTrainer
from airosentris.trainer.TrainerRegistry import TrainerRegistry


class BERTTrainer(BaseTrainer):
    def __init__(self, model_name="bert-base-cased", output_dir="train_output", learning_rate=2e-5, batch_size=32, num_epochs=10, logging_steps=500):
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.training_args = TrainingArguments(
            output_dir=output_dir,
            eval_strategy="steps",
            evaluation_strategy="steps",
            learning_rate=learning_rate,
            per_device_train_batch_size=batch_size,
            per_device_eval_batch_size=batch_size,
            num_train_epochs=num_epochs,
            weight_decay=0.01,
            save_steps=logging_steps,
            logging_steps=logging_steps,
            logging_dir=f"{output_dir}/logs",
            load_best_model_at_end=True,
            save_total_limit=1,
            # metric_for_best_model="accuracy",
            report_to="none",
            fp16=torch.cuda.is_available(), 
        )
        self.trainer = None
        self.data_collator = DefaultDataCollator(return_tensors="pt")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    def tokenize_function(self, dataset):
        return self.tokenizer(
            dataset["text"],
            padding="max_length",
            truncation=True,
            max_length=128,
        )

    def train(self, train_data, train_labels):
        print(f"Training data: {train_data}")
        print(f"Training labels: {train_labels}")

        num_labels = len(set(train_labels))

        train_data_list = [line.rsplit(":", 1) for line in train_data.strip().split("\n")]
        df = pd.DataFrame(train_data_list, columns=["text", "label"])
        df["label"] = df["label"].astype(int)

        dataset = Dataset.from_pandas(df)

        accuracies, precisions, recalls, f1_scores = [], [], [], []

        n_splits = min(5, num_labels)
        skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=42)

        for fold, (train_index, val_index) in enumerate(skf.split(df["text"], df["label"])):
            train_dataset = dataset.select(train_index).map(self.tokenize_function, batched=True)
            val_dataset = dataset.select(val_index).map(self.tokenize_function, batched=True)

            model = BertForSequenceClassification.from_pretrained(self.model_name, num_labels=num_labels).to(self.device)

            self.trainer = Trainer(
                model=model,
                args=self.training_args,
                train_dataset=train_dataset,
                eval_dataset=val_dataset,
                tokenizer=self.tokenizer,
                data_collator=self.data_collator,
            )

            self.trainer.train()

            predictions, label_ids, metrics = self.trainer.predict(val_dataset)
            predictions = torch.argmax(torch.tensor(predictions), dim=1)

            accuracies.append(accuracy_score(val_dataset["label"], predictions))
            precision, recall, f1, _ = precision_recall_fscore_support(val_dataset["label"], predictions, average="macro")
            precisions.append(precision)
            recalls.append(recall)
            f1_scores.append(f1)

        print(f"Average accuracy: {sum(accuracies) / len(accuracies)}")
        print(f"Average precision: {sum(precisions) / len(precisions)}")
        print(f"Average recall: {sum(recalls) / len(recalls)}")
        print(f"Average F1 score: {sum(f1_scores) / len(f1_scores)}")

    def evaluate(self, test_data, test_labels):
        print(f"Evaluating with test data: {test_data} and labels: {test_labels}")

        test_data_list = [line.rsplit(":", 1) for line in test_data.strip().split("\n")]
        df = pd.DataFrame(test_data_list, columns=["text", "label"])
        df["label"] = df["label"].astype(int)

        dataset = Dataset.from_pandas(df)

        tokenized_dataset = dataset.map(self.tokenize_function, batched=True)
        predictions = self.trainer.predict(tokenized_dataset)["predictions"]
        predictions = torch.argmax(torch.tensor(predictions), dim=1)

        accuracy = accuracy_score(dataset["label"], predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(dataset["label"], predictions, average="binary")

        print(f"Accuracy: {accuracy}")
        print(f"Precision: {precision}")
        print(f"Recall: {recall}")
        print(f"F1 score: {f1}")

    def save_model(self, file_path):
        print(f"Model saved to {file_path}")
        self.trainer.save_model(file_path)

    def load_model(self, file_path):
        print(f"Model loaded from {file_path}")
        self.trainer.model = BertForSequenceClassification.from_pretrained(file_path).to(self.device)



# Register the trainer with the Registry
TrainerRegistry.register_trainer('BERT', BERTTrainer)