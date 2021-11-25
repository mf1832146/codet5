from tokenizers import Tokenizer
from tokenizers.models import WordLevel
from tokenizers.trainers import WordLevelTrainer

# Initialize a tokenizer
from create_db import find_all_by_tag, connect_db

tokenizer = Tokenizer(WordLevel())
trainer = WordLevelTrainer(vocab_size=32000, min_frequency=3, special_tokens=[
    "<pad>",
    "<s>",
    "</s>",
    "<unk>",
    "<mask>"
])

# tokenizer.train(files=['train_code.txt', 'train_doc.txt'], trainer=trainer)

word_tokens = []

codes = connect_db().codes
results = find_all_by_tag(codes, 'train')

for result in results:
    word_tokens.extend(result['code_tokens'])
    word_tokens.extend(result['docstring_tokens'])

tokenizer.train_from_iterator(word_tokens, trainer=trainer, length=len(word_tokens))

# Save files to disk
tokenizer.save('./vocab/code_and_doc.vocab', pretty=True)

print(
    tokenizer.encode("<s> hello <unk> Don't you love 🤗 Transformers <mask> yes . </s>").tokens
)


