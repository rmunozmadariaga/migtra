ARG ACCOUNT_ID

ARG REGION

ARG BASE_LAYER_VERSION

#FROM ${ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/ms-bff-base-layer:${BASE_LAYER_VERSION}
FROM 041425181734.dkr.ecr.us-east-1.amazonaws.com/ms-bff-base-layer:1.0.2

COPY app/requirements.txt .

COPY app /app
