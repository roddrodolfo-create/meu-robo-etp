import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Captura apenas o texto do Objeto enviado pelo painel do celular
if len(sys.argv) > 1:
    objeto_etp = sys.argv[1]
else:
    print("❌ Erro: Nenhum objeto foi enviado pelo aplicativo.")
    sys.exit(1)

print(f"🤖 Robô Iniciado! Processando o objeto de ETP...")

# ==============================================================================
# CONFIGURAÇÃO DO NAVEGADOR COM MÁSCARA HUMANA (EVITA ERROS DE JAVASCRIPT)
# ==============================================================================
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Altera o User-Agent para o servidor não descobrir que é um robô rodando
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Inicia o navegador na nuvem
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    # ==============================================================================
    # INDO DIRETO PARA O PREENCHEDOR DE ETP
    # ==============================================================================
    print("🔗 Abrindo a tela direta do preenchedor de ETP...")
    
    # !!! SUBSTITUA A URL ABAIXO PELA URL DIRETA DA TELA DO SEU COMPRASNET ONDE COLA O OBJETO !!!
    driver.get("https://www.gov.br")  
    time.sleep(5)
    
    # Executa os passos de cliques e preenchimentos que você já tinha no seu robô original:
    print(f"📝 Inserindo o texto no campo Objeto: '{objeto_etp[:30]}...'")
    
    # (Cole aqui embaixo a continuação do seu código que interage com a tela do ETP)
    
    print("🎉 Processamento do ETP concluído com sucesso!")

except Exception as e:
    print(f"❌ Ocorreu uma falha no preenchimento do formulário: {e}")

finally:
    driver.quit()
    print("🔌 Processo encerrado.")
