from ray.rllib.algorithms.sac.sac import SACConfig
from ray.rllib.utils.metrics import (
    ENV_RUNNER_RESULTS,
    EPISODE_RETURN_MEAN,
    NUM_ENV_STEPS_SAMPLED_LIFETIME,
)

config = (
    SACConfig()
    # Enable new API stack and use EnvRunner.
    .api_stack(
        enable_rl_module_and_learner=True,
        enable_env_runner_and_connector_v2=True,
    )
    .env_runners(
        rollout_fragment_length=1,
        num_env_runners=0,
    )
    .environment(env="Pendulum-v1")
    .rl_module(
        model_config_dict={
            "fcnet_hiddens": [256, 256],
            "fcnet_activation": "relu",
            "post_fcnet_hiddens": [],
            "post_fcnet_activation": None,
            "post_fcnet_weights_initializer": "orthogonal_",
            "post_fcnet_weights_initializer_config": {"gain": 0.01},
        }
    )
    .training(
        initial_alpha=1.001,
        lr=3e-4,
        target_entropy="auto",
        n_step=1,
        tau=0.005,
        train_batch_size=256,
        target_network_update_freq=1,
        replay_buffer_config={
            "type": "PrioritizedEpisodeReplayBuffer",
            "capacity": 100000,
            "alpha": 1.0,
            "beta": 0.0,
        },
        num_steps_sampled_before_learning_starts=256,
    )
    .reporting(
        metrics_num_episodes_for_smoothing=5,
        min_sample_timesteps_per_iteration=1000,
    )
)

stop = {
    NUM_ENV_STEPS_SAMPLED_LIFETIME: 20000,
    f"{ENV_RUNNER_RESULTS}/{EPISODE_RETURN_MEAN}": -250.0,
}
