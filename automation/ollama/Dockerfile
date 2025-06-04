FROM ollama/ollama:latest

# Optional: copy your key (you’ve done this already)
WORKDIR /root/.ollama
COPY id_ed25519.pub .

# Expose Ollama API
EXPOSE 11434

# ✅ Correct CMD (just 'serve')
CMD ["serve"]
