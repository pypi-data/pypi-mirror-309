from typing import Optional, Dict, Any, List
from transformers import Trainer, TrainingArguments, AutoTokenizer, AutoModelForCausalLM
from llamarch.common.llm import LLM


class CustomDataset:
    def __init__(self, encodings):
        self.encodings = encodings

    def __getitem__(self, idx):
        # Prepare inputs and labels
        input_ids = self.encodings['input_ids'][idx]
        attention_mask = self.encodings['attention_mask'][idx]

        # Shift input_ids to create labels
        labels = input_ids.clone()
        labels[:-1] = input_ids[1:]  # Shift left by 1
        labels[-1] = -100  # Ignore the last token for the loss calculation

        return {
            'input_ids': input_ids,
            'attention_mask': attention_mask,
            'labels': labels
        }

    def __len__(self):
        return len(self.encodings['input_ids'])


class FineTuner:
    """
    Fine-tuner class for fine-tuning a Hugging Face language model (LLM) with custom data.

    Attributes
    ----------
    llm : LLM
        An instance of the LLM class, representing the language model to be fine-tuned.

    Methods
    -------
    fine_tune(texts, output_dir="./fine_tuned_model")
        Fine-tunes the LLM's model with the provided list of texts.
    """

    def __init__(self, llm: LLM):
        """
        Initializes the FineTuner with an LLM instance.

        Parameters
        ----------
        llm : LLM
            An instance of the LLM class to be fine-tuned.
        """
        self.llm = llm

    def fine_tune(self, texts: List[str], output_dir: str = "./fine_tuned_model"):
        """
        Fine-tunes the LLM model with the provided list of texts.

        This method tokenizes the input texts, prepares them into a dataset, and trains the model using
        the Hugging Face Trainer API. The fine-tuned model is saved to the specified output directory.

        Parameters
        ----------
        texts : List[str]
            A list of strings to be used for training the model.
        output_dir : str, optional
            The directory where the fine-tuned model will be saved (default is "./fine_tuned_model").

        Returns
        -------
        LLM
            The LLM instance updated to use the fine-tuned model.

        Raises
        ------
        ValueError
            If the model category of the LLM is not "huggingface".
        """
        if self.llm.model_category != "huggingface":
            raise ValueError(
                "Fine-tuning is only supported for Hugging Face models in this implementation.")

        # Load the model and tokenizer
        model = AutoModelForCausalLM.from_pretrained(self.llm.model_name)
        tokenizer = AutoTokenizer.from_pretrained(self.llm.model_name)
        # Set pad_token to eos_token
        tokenizer.pad_token = tokenizer.eos_token

        # Tokenize data
        encodings = tokenizer(
            texts,
            truncation=True,
            padding="max_length",
            max_length=512,  # Adjust max_length as needed
            return_tensors="pt"  # Return PyTorch tensors
        )

        # Create dataset from encodings
        train_dataset = CustomDataset(encodings)

        # Set training arguments
        training_args = TrainingArguments(
            output_dir=output_dir,
            eval_strategy="no",
            learning_rate=2e-5,
            weight_decay=0.01,
            num_train_epochs=3,
            per_device_train_batch_size=8,
            save_total_limit=2,  # Save only the last 2 models
            logging_dir='./logs',  # Directory for storing logs
            logging_steps=10,  # Log every 10 steps
        )

        # Initialize Trainer
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset
        )

        # Fine-tune the model
        trainer.train()

        # Save the fine-tuned model
        model.save_pretrained(output_dir)
        tokenizer.save_pretrained(output_dir)

        # Update the LLM instance to use the fine-tuned model
        self.llm.model_name = output_dir
        self.llm.model = self.llm._initialize_llm()

        return self.llm
