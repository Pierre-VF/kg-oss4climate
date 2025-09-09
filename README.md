# kg-oss4climate
Knowledge graph building for OSS in the climate space

Underlying tools:
- [Pydantic AI](https://ai.pydantic.dev/)
- [LangChain](https://python.langchain.com/docs/introduction/)


Interesting queries:

- `MATCH p=()-[:IS_IMPLEMENTED_IN|IS_FROM_ORGANISATION|IS_LICENSED_UNDER|IS_HOSTED_ON_DOMAIN]->() RETURN p LIMIT 2500;``shows the full graph
