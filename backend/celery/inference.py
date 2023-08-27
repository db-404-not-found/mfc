from pathlib import Path

import torch
from loguru import logger
from transformers import GPT2LMHeadModel, GPT2Tokenizer

PROJECT_PATH = Path("./backend")


class MultiFunctionalModel:
    def __init__(self):
        self.cuda = torch.cuda.is_available()
        self.train_dir = "train_output"
        premodel = GPT2LMHeadModel.from_pretrained(
            PROJECT_PATH / self.train_dir, local_files_only=True
        )
        try:
            self.tok = GPT2Tokenizer.from_pretrained(PROJECT_PATH / self.train_dir)
        except OSError as error:
            logger.exception("Upalo")
            raise error

        self.model = premodel.to("cuda" if self.cuda else "cpu")
        self.eot_token = "<|endoftext|>"
        self.question_token = "<|Вопрос:|> "
        self.answer_token = " <|Ответ:|> "
        self.max_length = 64

    def predict(
        self,
        question: str,
        do_sample=True,
        max_length=None,
        num_answers=3,
        repetition_penalty=5.0,
        top_k=5,
        top_p=0.98,
        temperature=1,
        num_beams=10,
        no_repeat_ngram_size=3,
    ) -> str:
        logger.info("Start predict")
        if max_length is None:
            max_length = self.max_length

        possible_tokens = [
            self.answer_token,
            "<|Ответ:|nbsp;",
            "<|Ответ:|nbsp",
            "<|Ответ :|>",
        ]
        input_ids = self.tok.encode(
            self.question_token + question, return_tensors="pt"
        ).to("cuda" if self.cuda else "cpu")
        out_ids = self.model.generate(
            input_ids,
            max_length=max_length,
            repetition_penalty=repetition_penalty,
            do_sample=do_sample,
            top_k=top_k,
            top_p=top_p,
            temperature=temperature,
            num_beams=num_beams,
            no_repeat_ngram_size=no_repeat_ngram_size,
            num_return_sequences=num_answers,
        )
        answers = list(map(self.tok.decode, out_ids))
        summary = ""
        for i, answer in enumerate(answers):
            for token in possible_tokens:
                found = answer.find(token)
                if found >= 0:
                    answer = answer[found + len(token) :]
                    break
            else:
                found = answer.find(self.question_token)
                if found >= 0:
                    answer = answer[found + len(self.question_token) :]
            if num_answers > 1:
                summary += ("" if i == 0 else "\n") + str(i + 1) + ". " + answer
            else:
                summary = answer
        logger.info("End of predict")
        return summary
