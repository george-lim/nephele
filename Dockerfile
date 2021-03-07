FROM public.ecr.aws/george-lim/firefox-lambda:1.0.1

ENV FIREFOX_BINARY_PATH=/opt/firefox/firefox

COPY requirements.txt .

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY src src
