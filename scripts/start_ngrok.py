from pyngrok import ngrok

if __name__ == '__main__':
    tunnel = ngrok.connect(8501, "http")
    print(tunnel.public_url)
    print("Tunnel started. Open the app in the browser.")
