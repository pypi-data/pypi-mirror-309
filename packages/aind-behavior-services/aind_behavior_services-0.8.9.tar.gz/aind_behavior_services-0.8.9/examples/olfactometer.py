import os

from aind_behavior_services.base import get_commit_hash
from aind_behavior_services.calibration import olfactometer as olf
from aind_behavior_services.session import AindBehaviorSessionModel
from aind_behavior_services.utils import utcnow

channels_config = {
    olf.OlfactometerChannel.Channel0: olf.OlfactometerChannelConfig(
        channel_index=olf.OlfactometerChannel.Channel0,
        channel_type=olf.OlfactometerChannelType.ODOR,
        flow_rate=100,
        odorant="Banana",
        odorant_dilution=0.1,
    ),
    olf.OlfactometerChannel.Channel1: olf.OlfactometerChannelConfig(
        channel_index=olf.OlfactometerChannel.Channel1,
        channel_type=olf.OlfactometerChannelType.ODOR,
        flow_rate=100,
        odorant="Strawberry",
        odorant_dilution=0.1,
    ),
    olf.OlfactometerChannel.Channel2: olf.OlfactometerChannelConfig(
        channel_index=olf.OlfactometerChannel.Channel2,
        channel_type=olf.OlfactometerChannelType.ODOR,
        flow_rate=100,
        odorant="Apple",
        odorant_dilution=0.1,
    ),
    olf.OlfactometerChannel.Channel3: olf.OlfactometerChannelConfig(
        channel_index=olf.OlfactometerChannel.Channel3, channel_type=olf.OlfactometerChannelType.CARRIER, odorant="Air"
    ),
}

calibration = olf.OlfactometerCalibration(
    input=olf.OlfactometerCalibrationInput(), output=olf.OlfactometerCalibrationOutput()
)

calibration_logic = olf.CalibrationLogic(
    task_parameters=olf.CalibrationParameters(
        channel_config=channels_config,
        full_flow_rate=1000,
        n_repeats_per_stimulus=10,
        time_on=1,
        time_off=1,
    )
)

calibration_session = AindBehaviorSessionModel(
    root_path="C:\\Data",
    date=utcnow(),
    allow_dirty_repo=False,
    experiment="OlfactometerCalibration",
    experiment_version="0.0.0",
    subject="Olfactometer",
    commit_hash=get_commit_hash(),
)

rig = olf.CalibrationRig(
    rig_name="OlfactometerRig",
    harp_olfactometer=olf.Olfactometer(port_name="COM4"),
    harp_analog_input=olf.HarpAnalogInput(port_name="COM5"),
    harp_clock_generator=olf.HarpClockGenerator(port_name="COM6"),
)


seed_path = "local/olfactometer_{suffix}.json"
os.makedirs(os.path.dirname(seed_path), exist_ok=True)

with open(seed_path.format(suffix="calibration_logic"), "w") as f:
    f.write(calibration_logic.model_dump_json(indent=3))
with open(seed_path.format(suffix="session"), "w") as f:
    f.write(calibration_session.model_dump_json(indent=3))
with open(seed_path.format(suffix="rig"), "w") as f:
    f.write(rig.model_dump_json(indent=3))
