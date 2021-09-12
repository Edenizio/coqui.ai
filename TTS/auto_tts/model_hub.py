import os

from recipes.ljspeech.glow_tts.train_glowtts import config as glowtts_config
from recipes.ljspeech.hifigan.train_hifigan import config as hifigan_config
from recipes.ljspeech.multiband_melgan.train_multiband_melgan import config as multiband_melgan_config
from recipes.ljspeech.univnet.train import config as univnet_config
from recipes.ljspeech.vits_tts.train_vits import config as vits_config
from recipes.ljspeech.wavegrad.train_wavegrad import config as wavegrad_config
from recipes.ljspeech.wavernn.train_wavernn import config as waverrn_config
from TTS.tts.configs.glow_tts_config import GlowTTSConfig
from TTS.tts.configs.tacotron2_config import Tacotron2Config
from TTS.auto_tts.utils import pick_glowtts_encoder

class TtsModels:
    def __init__(
        self, batch_size: int, mixed_precision: bool, learning_rate: float, epochs: int,
            output_path=os.path.dirname(os.path.abspath(__file__))
    ):

        self.batch_size = batch_size
        self.output_path = output_path
        self.mixed_precision = mixed_precision
        self.learning_rate = learning_rate
        self.epochs = epochs

    def single_speaker_tacotron2_base(
        self, audio, dataset, dla=0.25, pla=0.25, ga=5.0, forward_attn=True, location_attn=True
    ):
        config = Tacotron2Config(
            run_name="single_speaker_tacotron2",
            audio=audio,
            batch_size=self.batch_size,
            eval_batch_size=int(self.batch_size / 2),
            r=2,
            grad_clip=1,
            lr=self.learning_rate,
            decoder_loss_alpha=dla,
            postnet_loss_alpha=pla,
            postnet_diff_spec_alpha=0.25,
            decoder_diff_spec_alpha=0.25,
            decoder_ssim_alpha=0.25,
            postnet_ssim_alpha=0.25,
            ga_alpha=ga,
            stopnet_pos_weight=15.0,
            memory_size=-1,
            phoneme_cache_path=os.path.join(self.output_path, "phoneme_cache"),
            prenet_type="original",
            prenet_dropout=True,
            attention_type="original",
            attention_heads=5,
            attention_norm="sigmoid",
            windowing=False,
            use_forward_attn=forward_attn,
            forward_attn_mask=False,
            transition_agent=False,
            location_attn=location_attn,
            stopnet=True,
            separate_stopnet=True,
            print_step=25,
            save_step=10000,
            checkpoint=True,
            text_cleaner="basic_cleaners",
            num_loader_workers=6,
            num_eval_loader_workers=6,
            min_seq_len=6,
            max_seq_len=150,
            output_path=self.output_path,
            datasets=[dataset],
        )
        return config

    def single_speaker_tacotron2_DDC(
        self, audio, dataset, dla=0.25, pla=0.25, ga=5.0, forward_attn=False, location_attn=True
    ):
        config = Tacotron2Config(
            audio=audio,
            run_name="ljspeech-ddc",
            run_description="tacotron2 with double decoder consistency.",
            batch_size=self.batch_size,
            eval_batch_size=self.batch_size // 2,
            mixed_precision=False,
            loss_masking=True,
            decoder_loss_alpha=dla,
            postnet_loss_alpha=pla,
            postnet_diff_spec_alpha=0.25,
            decoder_diff_spec_alpha=0.25,
            decoder_ssim_alpha=0.25,
            postnet_ssim_alpha=0.25,
            ga_alpha=ga,
            stopnet_pos_weight=15.0,
            run_eval=True,
            test_delay_epochs=10,
            max_decoder_steps=1000,
            grad_clip=0.05,
            epochs=self.epochs,
            lr=self.learning_rate,
            memory_size=-1,
            prenet_type="original",
            use_forward_attn=forward_attn,
            prenet_dropout=True,
            attention_type="original",
            location_attn=location_attn,
            double_decoder_consistency=True,
            ddc_r=6,
            attention_norm="sigmoid",
            r=6,
            gradual_training=[
                [0, 6, self.batch_size],
                [10000, 4, self.batch_size // 2],
                [50000, 3, self.batch_size // 2],
                [100000, 2, self.batch_size // 2],
            ],
            stopnet=True,
            separate_stopnet=True,
            print_step=25,
            print_eval=False,
            plot_step=100,
            save_step=10000,
            checkpoint=True,
            text_cleaner="phoneme_cleaners",
            num_loader_workers=4,
            num_eval_loader_workers=4,
            batch_group_size=4,
            min_seq_len=6,
            max_seq_len=180,
            compute_input_seq_cache=True,
            phoneme_cache_path=os.path.join(self.output_path, "phoneme_cache"),
            output_path=self.output_path,
            use_phonemes=False,
            phoneme_language="en-us",
            datasets=[dataset],
        )
        return config

    def single_speaker_tacotron2_DCA(
        self, audio, dataset, dla=0.25, pla=0.25, ga=5.0, forward_attn=False, location_attn=True
    ):
        config = Tacotron2Config(
            audio=audio,
            run_name="ljspeech-dca",
            run_description="tacotron2 with dynamic conv attention.",
            batch_size=self.batch_size,
            eval_batch_size=self.batch_size // 2,
            mixed_precision=True,
            loss_masking=True,
            decoder_loss_alpha=dla,
            postnet_loss_alpha=pla,
            postnet_diff_spec_alpha=0.25,
            decoder_diff_spec_alpha=0.25,
            decoder_ssim_alpha=0.25,
            postnet_ssim_alpha=0.25,
            ga_alpha=ga,
            stopnet_pos_weight=15.0,
            run_eval=True,
            test_delay_epochs=10,
            max_decoder_steps=1000,
            grad_clip=0.05,
            epochs=self.epochs,
            lr=self.learning_rate,
            memory_size=-1,
            prenet_type="original",
            use_forward_attn=forward_attn,
            prenet_dropout=True,
            attention_type="dynamic_convolution",
            location_attn=location_attn,
            attention_norm="sigmoid",
            r=2,
            stopnet=True,
            separate_stopnet=True,
            print_step=25,
            plot_step=100,
            print_eval=False,
            save_step=10000,
            checkpoint=True,
            text_cleaner="phoneme_cleaners",
            num_loader_workers=4,
            num_eval_loader_workers=4,
            batch_group_size=4,
            min_seq_len=6,
            max_seq_len=180,
            compute_input_seq_cache=True,
            output_path=self.output_path,
            phoneme_cache_path=os.path.join(self.output_path, "phoneme_cache"),
            use_phonemes=False,
            phoneme_language="en-us",
            datasets=[dataset],
        )
        return config

    def single_speaker_glow_tts(self, audio, dataset, encoder):
        encoder_type = pick_glowtts_encoder(encoder)
        glowtts_config.audio = audio
        glowtts_config.batch_size = self.batch_size
        glowtts_config.eval_batch_size = self.batch_size // 2
        glowtts_config.epochs = self.epochs
        glowtts_config.output_path = self.output_path
        glowtts_config.lr = self.learning_rate
        glowtts_config.mixed_precision = self.mixed_precision
        glowtts_config.encoder_type = encoder_type
        glowtts_config.datasets = [dataset]
        config = glowtts_config
        return config

    def sc_glow_tts(self, audio, dataset, speaker_file, encoder):
        encoder_type = pick_glowtts_encoder(encoder)
        config = GlowTTSConfig(
            audio=audio,
            run_name="multispeaker glow tts",
            run_description="glow tts for multispeaker datasets",
            batch_size=self.batch_size,
            eval_batch_size=self.batch_size // 2,
            mixed_precision=self.mixed_precision,
            run_eval=True,
            test_delay_epochs=-1,
            print_eval=False,
            print_step=25,
            plot_step=100,
            model_param_stats=False,
            save_step=10000,
            num_loader_workers=8,
            num_eval_loader_workers=8,
            use_noise_augment=False,
            output_path=self.output_path,
            use_phonemes=True,
            use_espeak_phonemes=True,
            phoneme_language="en",
            compute_input_seq_cache=False,
            test_sentences_file=None,
            phoneme_cache_path=os.path.join(self.output_path, "phoneme_cache"),
            batch_group_size=0,
            loss_masking=True,
            min_seq_len=2,
            max_seq_len=500,
            compute_f0=False,
            add_blank=True,
            use_speaker_embedding=True,
            use_d_vector_file=True,
            d_vector_dim=256,
            encoder_type=encoder_type,
            use_encoder_prenet=True,
            hidden_channels_dp=256,
            hidden_channels_dec=192,
            hidden_channels_enc=192,
            dropout_p_dp=0.1,
            dropout_p_dec=0.05,
            mean_only=True,
            out_channels=80,
            num_flow_blocks_dec=12,
            inference_noise_scale=0.0,
            kernel_size_dec=5,
            dilation_rate=1,
            num_block_layers=4,
            num_speakers=0,
            num_splits=4,
            num_squeeze=2,
            sigmoid_scale=False,
            data_dep_init_steps=10,
            style_wav_for_test=None,
            length_scale=1.0,
            d_vector_file=speaker_file,
            grad_clip=5.0,
            lr=self.learning_rate,
            r=1,
            datasets=[dataset],
        )
        return config

    def single_speaker_vits_tts(self, audio, dataset):
        vits_config.audio = audio
        vits_config.datasets = [dataset]
        vits_config.lr_gen = self.learning_rate
        vits_config.lr_disc = self.learning_rate
        vits_config.batch_size = self.batch_size
        vits_config.eval_batch_size = self.batch_size // 2
        vits_config.mixed_precision = self.mixed_precision
        vits_config.output_path = self.output_path
        config = vits_config
        return config

    def vctk_vits_tts(self, audio, dataset, speaker_file):
        vits_config.audio = audio
        vits_config.datasets = [dataset]
        vits_config.lr_gen = self.learning_rate
        vits_config.lr_disc = self.learning_rate
        vits_config.batch_size = self.batch_size
        vits_config.eval_batch_size = self.batch_size // 2
        vits_config.mixed_precision = self.mixed_precision
        vits_config.output_path = self.output_path
        vits_config.use_speaker_embedding = True
        vits_config.num_speakers = 109
        vits_config.speaker_embedding_channels = 256
        vits_config.speakers_file = speaker_file
        vits_config.num_chars = 179



class VocoderModels:
    def __init__(
        self,
        batch_size,
        mixed_precision,
        generator_learning_rate,
        discriminator_learning_rate,
        epochs,
        output_path=os.path.dirname(os.path.abspath(__file__)),
    ):
        self.batch_size = batch_size
        self.output_path = output_path
        self.mixed_precision = mixed_precision
        self.generator_lr = generator_learning_rate
        self.discriminator_lr = discriminator_learning_rate
        self.epochs = epochs

    def hifi_gan(self, audio, data_path):
        hifigan_config.data_path = data_path
        hifigan_config.audio = audio
        hifigan_config.batch_size = self.batch_size
        hifigan_config.eval_batch_size = self.batch_size // 2
        hifigan_config.output_path = self.output_path
        hifigan_config.mixed_precision = self.mixed_precision
        hifigan_config.epochs = self.epochs
        hifigan_config.lr_gen = self.generator_lr
        hifigan_config.lr_disc = self.discriminator_lr
        config = hifigan_config
        return config

    def wavegrad(self, audio, datapath):
        wavegrad_config.audio = audio
        wavegrad_config.data_path = datapath
        wavegrad_config.batch_size = self.batch_size
        wavegrad_config.eval_batch_size = self.batch_size // 2
        wavegrad_config.output_path = self.output_path
        wavegrad_config.mixed_precision = self.mixed_precision
        wavegrad_config.epochs = self.epochs
        wavegrad_config.lr_gen = self.generator_lr
        wavegrad_config.lr_disc = self.discriminator_lr
        config = wavegrad_config
        return config

    def multiband_melgan(self, audio, data_path):
        multiband_melgan_config.audio = audio
        multiband_melgan_config.data_path = data_path
        multiband_melgan_config.batch_size = self.batch_size
        multiband_melgan_config.eval_batch_size = self.batch_size // 2
        multiband_melgan_config.output_path = self.output_path
        multiband_melgan_config.mixed_precision = self.mixed_precision
        multiband_melgan_config.epochs = self.epochs
        multiband_melgan_config.lr_gen = self.generator_lr
        multiband_melgan_config.lr_disc = self.discriminator_lr
        config = multiband_melgan_config
        return config

    def univnet(self, audio, data_path):
        univnet_config.audio = audio
        univnet_config.data_path = data_path
        univnet_config.batch_size = self.batch_size
        univnet_config.eval_batch_size = self.batch_size // 2
        univnet_config.output_path = self.output_path
        univnet_config.mixed_precision = self.mixed_precision
        univnet_config.epochs = self.epochs
        univnet_config.lr_gen = self.generator_lr
        univnet_config.lr_disc = self.discriminator_lr
        config = univnet_config
        return config

    def wavernn(self, audio, data_path):
        waverrn_config.audio = audio
        waverrn_config.data_path = data_path
        waverrn_config.batch_size = self.batch_size
        waverrn_config.eval_batch_size = self.batch_size // 2
        waverrn_config.output_path = self.output_path
        waverrn_config.mixed_precision = self.mixed_precision
        waverrn_config.epochs = self.epochs
        waverrn_config.lr_gen = self.generator_lr
        waverrn_config.lr_disc = self.discriminator_lr
        config = waverrn_config
        return config
