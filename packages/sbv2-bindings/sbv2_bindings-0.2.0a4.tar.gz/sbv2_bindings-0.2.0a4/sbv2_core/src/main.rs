use std::env;
use std::fs;

#[cfg(feature = "std")]
fn main_inner() -> anyhow::Result<()> {
    use sbv2_core::tts;
    dotenvy::dotenv_override().ok();
    env_logger::init();
    let text = fs::read_to_string("content.txt")?;
    let ident = "aaa";
    let mut tts_holder = tts::TTSModelHolder::new(
        &fs::read(env::var("BERT_MODEL_PATH")?)?,
        &fs::read(env::var("TOKENIZER_PATH")?)?,
        env::var("HOLDER_MAX_LOADED_MODElS")
            .ok()
            .and_then(|x| x.parse().ok()),
    )?;
    #[cfg(not(feature = "aivmx"))]
    {
        tts_holder.load_sbv2file(ident, fs::read(env::var("MODEL_PATH")?)?)?;
    }
    #[cfg(feature = "aivmx")]
    {
        tts_holder.load_aivmx(ident, fs::read(env::var("MODEL_PATH")?)?)?;
    }

    let audio =
        tts_holder.easy_synthesize(ident, &text, 0, 0, tts::SynthesizeOptions::default())?;
    fs::write("output.wav", audio)?;

    Ok(())
}

#[cfg(not(feature = "std"))]
fn main_inner() -> anyhow::Result<()> {
    Ok(())
}

fn main() {
    if let Err(e) = main_inner() {
        println!("Error: {e}");
    }
}
