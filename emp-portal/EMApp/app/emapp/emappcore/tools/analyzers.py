from elasticsearch_dsl import analyzer, tokenizer

trigram_analyzer = analyzer('trigram_analyzer',
                            tokenizer=tokenizer('trigram', 'nGram', min_gram=3, max_gram=3),
                            filter=['lowercase']
                            )


email_analyzer = analyzer(
    'email_analyzer',
    tokenizer=tokenizer('uax_url_email'),
    filter=['lowercase']
)
