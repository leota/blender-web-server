import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration
from config import Settings

env = Settings()

def init_sentry():
    sentry_sdk.init(
        dsn=env.SENTRY_DSN,
        environment=env.ENVIRONMENT,
        enable_tracing=True,
        integrations=[
            StarletteIntegration(
                transaction_style="endpoint"
            ),
            FastApiIntegration(
                transaction_style="endpoint"
            ),
        ],
        traces_sample_rate=0.1,
        profiles_sample_rate=1.0,
    )

