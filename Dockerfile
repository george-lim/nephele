FROM lambci/lambda:build-python3.8

# Copy requirements.txt
COPY requirements.txt /var/artifacts/requirements.txt

# Download Chromium artifacts
WORKDIR /var/artifacts/chromium
RUN curl -sLO https://github.com/alixaxel/chrome-aws-lambda/raw/v5.5.0/bin/aws.tar.br \
  && curl -sLO https://github.com/alixaxel/chrome-aws-lambda/raw/v5.5.0/bin/chromium.br \
  && curl -sLO https://github.com/alixaxel/chrome-aws-lambda/raw/v5.5.0/bin/swiftshader.tar.br

# Download Python requirements
WORKDIR /var/artifacts
RUN python3 -m pip install --no-cache-dir requests==2.25.1 \
  && python3 -m pip install --no-cache-dir -r requirements.txt -t python \
  && find python -name '*.so' -exec strip {} \;

# Package layer artifacts
RUN zip -r chromium.zip chromium \
  && zip -r requirements.zip python \
  && rm -r chromium python requirements.txt
