from data.analyze_data import SECTORS
from pipeline.pipeline import run_pipeline
from config.user_profile import USER_PROFILE

money=USER_PROFILE["money"]
risk=USER_PROFILE["risk"]

#for sector,symbols in SECTORS.items():
#   for symbol in symbols:
#        result = run_pipeline(
#           symbol,
#            money,
#            risk
#        )

result = run_pipeline(
            "QQQ",
            money,
            risk
        )
