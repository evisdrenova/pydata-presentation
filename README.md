# Introduction

This is a sample repo of how to use Benthos + python to build a synthetic data pipeline. I presented this at the Pydata Seattle talk on 5/16/2024.

In order to run this project, download the Benthos CLI - `brew install benthos`. This allows you to run benthos config files locally.

You'll also need to stand up two postgres databases that have mock data. Make sure you update the dsn in the `input` field in the benthos configs.

The models hosted on a flask server at endpoints `/fit` and `/sample`.
