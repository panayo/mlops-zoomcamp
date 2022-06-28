from prefect.deployments import DeploymentSpec
from prefect.orion.schemas.schedules import CronSchedule
from prefect.flow_runners import SubprocessFlowRunner


DeploymentSpec(
    flow_location="score.py",
    name="ride_duration_prediction",
    parameters={
        "taxi_type": "green",
        "run_id": "c6fa6d5c0adf4731ab38902e80068865"},
    flow_storage="79724b2d-27c0-4fc1-8dc5-7143c46d56c0",
    schedule=CronSchedule(cron="0 3 2 * *"),
    flow_runner=SubprocessFlowRunner(),
    tags=["ml"]
)