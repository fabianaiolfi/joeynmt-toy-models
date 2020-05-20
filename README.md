# joeynmt-toy-models

This repo is just a collection of scripts showing how to install [JoeyNMT](https://github.com/joeynmt/joeynmt), preprocess
data, train and evaluate models.

# Requirements

- This only works on a Unix-like system, with bash.
- Python 3 must be installed on your system, i.e. the command `python3` must be available
- Make sure virtualenv is installed on your system. To install, e.g.

    `pip install virtualenv`

# Steps

Clone this repository in the desired place and check out the correct branch:

    git clone https://github.com/bricksdont/joeynmt-toy-models
    cd joeynmt-toy-models
    checkout ex4

Create a new virtualenv that uses Python 3. Please make sure to run this command outside of any virtual Python environment:

    ./scripts/make_virtualenv.sh

**Important**: Then activate the env by executing the `source` command that is output by the shell script above.

Download and install required software:

    ./scripts/download_install_packages.sh

Download and split data:

    ./scripts/download_split_data.sh

Preprocess data:

    ./scripts/preprocess.sh

Then finally train a model:

    ./scripts/train.sh

The training process can be interrupted at any time, and the best checkpoint will always be saved.

Evaluate a trained model with

    ./scripts/evaluate.sh


***

# Documentation MT Exercise 5

## 2. Experiments with Byte Pair Encoding

### Setup
- Fork `https://github.com/bricksdont/joeynmt-toy-models` to your own Github account
- Switch to branch `ex5`
- Create virtualenv by running `./scripts/make_virtualenv.sh`
- Download and install the required software: `./scripts/download_install_packages.sh`
- Download the required data: `./scripts/download_data.sh`
- If the data is not parallel, try this:
```bash
wget https://files.ifi.uzh.ch/cl/archiv/2020/mt20/data.ex5.tar.gz
tar -xzvf data.ex5.tar.gz
```



### Sub-sample Parallel Training Data
For this exercise I chose the language pair [German and Italian](https://youtu.be/q69v7KypXR8?t=203), with the source language being German.
To randomly subsample the parallel training data, execute these [commands](https://stackoverflow.com/a/49037661):
```bash
cd data
shuf -n 100000 --random-source=train.de-it.de <(cat -n train.de-it.de) | sort -n | cut -f2- > subsample.train.de-it.de
shuf -n 100000 --random-source=train.de-it.de <(cat -n train.de-it.it) | sort -n | cut -f2- > subsample.train.de-it.it
cd ..
```
If you're having trouble with `shuf`, take a look at [this](https://apple.stackexchange.com/a/142864).



### Preprocessing: Tokenization
Execute the following commands to perform tokenization:
```bash
# Train
cat data/subsample.train.de-it.de | tools/moses-scripts/scripts/tokenizer/tokenizer.perl > data/subsample.tokenized.train.de-it.de
cat data/subsample.train.de-it.it | tools/moses-scripts/scripts/tokenizer/tokenizer.perl > data/subsample.tokenized.train.de-it.it

# Test
cat data/test.de-it.de | tools/moses-scripts/scripts/tokenizer/tokenizer.perl > data/tokenized.test.de-it.de
cat data/test.de-it.it | tools/moses-scripts/scripts/tokenizer/tokenizer.perl > data/tokenized.test.de-it.it

# Dev
cat data/dev.de-it.de | tools/moses-scripts/scripts/tokenizer/tokenizer.perl > data/tokenized.dev.de-it.de
cat data/dev.de-it.it | tools/moses-scripts/scripts/tokenizer/tokenizer.perl > data/tokenized.dev.de-it.it
```
_Sidenote: The input language in `tokenizer.perl` seems to be set to `en`. Not sure if this has a big effect on the final outcome, but may be something to look at later on._



### Training word-level model with JoeyNMT

1. Adjust configuration
To train a word-level model, I cloned `low_resource_example.yaml` to `low_resource_word_level.yaml` and made the following adjustments:
- Set `src_voc_limit` to `2000`
- Set `trg_voc_limit` to `2000`
- Set `beam_size` to `5`
- Set a `model_dir`

2. Train word-level language model
To train a word-level model, run the following command:
```bash
CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=4 python3 -m joeynmt train configs/low_resource_word_level.yaml
```



### Training BPE-level model with JoeyNMT

1. Learn BPE model
```bash
subword-nmt learn-joint-bpe-and-vocab \
-i data/subsample.tokenized.train.de-it.de data/subsample.tokenized.train.de-it.it \
--write-vocabulary data/bpe_vocab_{Vocabulary Size}/de.vocab data/bpe_vocab_{Vocabulary Size}/it.vocab \
-s {Vocabulary Size} --total-symbols -o data/bpe_vocab_{Vocabulary Size}/de-it.bpe
```

2. Apply BPE model to data
```bash
# Source Train
subword-nmt apply-bpe -c data/bpe_vocab_{Vocabulary Size}/de-it.bpe \
--vocabulary data/bpe_vocab_{Vocabulary Size}/de.vocab \
--vocabulary-threshold 10 \
< data/subsample.tokenized.train.de-it.de > data/bpe_vocab_{Vocabulary Size}/bpe.subsample.tokenized.train.de-it.de

# Source Test
subword-nmt apply-bpe -c data/bpe_vocab_{Vocabulary Size}/de-it.bpe \
--vocabulary data/bpe_vocab_{Vocabulary Size}/de.vocab \
--vocabulary-threshold 10 \
< data/tokenized.test.de-it.de > data/bpe_vocab_{Vocabulary Size}/bpe.tokenized.test.de-it.de

# Source Dev
subword-nmt apply-bpe -c data/bpe_vocab_{Vocabulary Size}/de-it.bpe \
--vocabulary data/bpe_vocab_{Vocabulary Size}/de.vocab \
--vocabulary-threshold 10 \
< data/tokenized.dev.de-it.de > data/bpe_vocab_{Vocabulary Size}/bpe.tokenized.dev.de-it.de

# Target Train
subword-nmt apply-bpe -c data/bpe_vocab_{Vocabulary Size}/de-it.bpe \
--vocabulary data/bpe_vocab_{Vocabulary Size}/it.vocab \
--vocabulary-threshold 10 \
< data/subsample.tokenized.train.de-it.it > data/bpe_vocab_{Vocabulary Size}/bpe.subsample.tokenized.train.de-it.it

# Target Test
subword-nmt apply-bpe -c data/bpe_vocab_{Vocabulary Size}/de-it.bpe \
--vocabulary data/bpe_vocab_{Vocabulary Size}/it.vocab \
--vocabulary-threshold 10 \
< data/tokenized.test.de-it.it > data/bpe_vocab_{Vocabulary Size}/bpe.tokenized.test.de-it.it

# Target Dev
subword-nmt apply-bpe -c data/bpe_vocab_{Vocabulary Size}/de-it.bpe \
--vocabulary data/bpe_vocab_{Vocabulary Size}/it.vocab \
--vocabulary-threshold 10 \
< data/tokenized.dev.de-it.it > data/bpe_vocab_{Vocabulary Size}/bpe.tokenized.dev.de-it.it
```

3. Build single vocabulary file
```bash
python3 tools/joeynmt/scripts/build_vocab.py \
data/bpe_vocab_{Vocabulary Size}/bpe.subsample.tokenized.train.de-it.de data/bpe_vocab_{Vocabulary Size}/bpe.subsample.tokenized.train.de-it.it \
--output_path data/bpe_vocab_{Vocabulary Size}/de-it.vocab
```

4. Train BPE-level language model
To train a BPE-level model, run the following command:
```bash
CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=4 python3 -m joeynmt train configs/low_resource_bpe_level_{Vocabulary Size}.yaml # my local device
CUDA_VISIBLE_DEVICES=0 OMP_NUM_THREADS=16 python3 -m joeynmt train configs/low_resource_bpe_level_{Vocabulary Size}.yaml # GCP VM
```



### Evaluation
Evaluation of the models on the test set, with detokenized, case-sensitive BLEU.

1. Detokenize model hypothesis:
```bash
cat models/{Model}/{Best Validation Result}.hyps.test | tools/moses-scripts/scripts/tokenizer/detokenizer.perl > models/{Model}/{Best Validation Result}.detokenized.hyps.test
```

2. Compute BLEU score using sacrebleu:
```bash
cat models/{Model}/{Best Validation Result}.detokenized.hyps.test | sacrebleu data/test.de-it.it
```

##### BLEU Score Comparisons
| Model | Use BPE | Vocabulary Size | BLEU |
|-------|---------|-----------------|------|
| (a)   | No      | 2000            | 2.0  |
| (b)   | Yes     | 1000            | 7.7  |
| (c)   | Yes     | 2000            | 7.4  |
| (d)   | Yes     | 3000            | 3.0  |
| (e)   | Yes     | 4000            | 3.6  |
| (f)   | Yes     | 8000            | 0.7  |

The BLEU score peaks around a vocabulary size of 1-2k when using BPE. As discussed in the tutorial, all results are to be regarded with caution due to the small training size and low amount of epochs.

3. Manually check translation
`low_resource_word_level`
Every sentence contains a `<unk>`, sometimes more than half the tokens in the sentence are unknown. This is probably due to the low vocabulary treshold.

`low_resource_bpe_level_1k` and `low_resource_bpe_level_2k`
No `<unk>` to be seen, which was to be expected. By just eyeballing the translations, sentences mostly seem to look like complete sentences. Now and then there are nonsensical word repetitions like "Getro , Betro , Betrg , Betrg , Betrg , Betrg , Scag".

`low_resource_bpe_level_3k` and `low_resource_bpe_level_4k`
I can't really see a difference to the 1k and 2k translations. This translation way worse according to the BLEU score, but I couldn't tell.

`low_resource_bpe_level_8k`
Lots of repetition, my favourite being: "In effetti , in realtà , il mondo , il mondo , il mondo , il mondo , il mondo , il mondo , il mondo , il mondo".



## 3. Impact of beam size on translation quality

### Translating with different beam sizes
Using the best model (vocabulary size: 1k), we can now perform translations and adjust the beam size each time.
The beam size can be adjusted manually in `configs/low_resource_bpe_level_1k.yaml` for each time the following scripts are executed:
```bash
# Translate test file
python3 -m joeynmt translate configs/low_resource_bpe_level_1k.yaml < data/test.de-it.de --output_path beam_size/{Beam Size}.hyps.test

# Detokenize hypothesis
cat beam_size/{Beam Size}.hyps.test | tools/moses-scripts/scripts/tokenizer/detokenizer.perl > beam_size/{Beam Size}.detokenized.hyps.test

# Calculate BLEU score
cat beam_size/{Beam Size}.detokenized.hyps.test | sacrebleu data/test.de-it.it
```

### Graph
[beam_size/plot_output.png]
Source: `beam_size/plot_script.py`

The highest BLEU score is achieved with a beam size of 1, which is – as far as I have understood – not actually a beam search but rather a greedy search. The higher the beam size, the lower the BLEU score and also the longer it takes to produce the translation.
I have the feeling that my results are slightly off due to the constraints of this exercise (small training data, few epochs) and that a beam size of around 5 would produce the best BLEU score with a properly functioning model.
