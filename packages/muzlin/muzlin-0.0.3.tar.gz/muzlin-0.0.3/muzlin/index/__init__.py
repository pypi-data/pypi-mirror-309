import apipkg

# Implement lazy loading
apipkg.initpkg(__name__, {
    'BaseIndex': 'muzlin.index.base:BaseIndex',
    'LangchainIndex': 'muzlin.index.langchain:LangchainIndex',
    'LlamaIndex': 'muzlin.index.llama_index:LlamaIndex',
})
