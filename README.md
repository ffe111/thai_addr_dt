# Thai Address Tagging API

English | [ภาษาไทย](README.th.md)

Extract Thai address entities with transformer-based named entity recognition (NER), then use reference data to match provinces, districts, subdistricts, and postal codes. The FastAPI service also attempts to extract names, organizations, and phone numbers when present.

## Quick start

From the repository root, build and run the container:

```bash
docker build -t thai-address-tagging .
docker run --rm -p 127.0.0.1:8080:8080 thai-address-tagging
```

For local development, use Python 3.11 (the version in the [Dockerfile](Dockerfile)), install [`requirements.txt`](requirements.txt) in a virtual environment, and run `python main.py`. The service loads the [`F311/addrthner`](https://huggingface.co/F311/addrthner) model on CPU at startup, so first startup needs network access if the model is not cached. The checked-in Compose file maps port 8000; the application listens on **8080**, so use the Docker command above unless you adjust the mapping.

## Try the API

Open [Swagger UI](http://localhost:8080/docs) and run `POST /addr-detect/address-check` with this synthetic request:

```json
{"text":"ต.สุเทพ อ.เมืองเชียงใหม่ จ.เชียงใหม่ 50200"}
```

The response contains the original `text` and an `address` object. Extracted fields may be incomplete when the model or reference data cannot resolve the input. The prototype can print extracted entities to stdout; keep real personal data out of demos, shared logs, and issue reports.

Start with [the API route](main.py), [the extraction and matching pipeline](thaiAddressTag/tag.py), or compare the [dictionary-based API](https://github.com/ffe111/address_detection_api).

<!-- Maintainers: Update the English README first, then mirror the change in README.th.md. -->
