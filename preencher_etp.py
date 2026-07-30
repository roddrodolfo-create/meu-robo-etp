import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ==============================================================================
# CONFIGURAÇÕES DE ACESSO PROTEGIDAS (SUAS CREDENCIAIS FIXAS)
# ==============================================================================
CPF_FIXO = "000.000.000-00"     # Digite aqui o CPF que o robô usará para logar
SENHA_FIXA = "SuaSenhaAqui"     # Digite aqui a senha do GOV.BR correspondente

# Captura o texto do Objeto enviado pelo painel do celular
if len(sys.argv) > 1:
    objeto_etp = sys.argv[1]
else:
    print("❌ Erro: Nenhum objeto foi enviado pelo aplicativo.")
    sys.exit(1)

print(f"🤖 Robô Iniciado! Processando o objeto: '{objeto_etp[:30]}...'")

# ==============================================================================
# CONFIGURAÇÃO DO NAVEGADOR PARA RODAR NA NUVEM (OBRIGATÓRIO)
# ==============================================================================
chrome_options = Options()
chrome_options.add_argument("--headless")  # Roda oculto nos servidores
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920,1080")

# Instala e inicia o navegador automaticamente na nuvem
servico = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=servico, options=chrome_options)
wait = WebDriverWait(driver, 20)

try:
    # 1. ACESSA O PORTAL DE LOGIN DO GOVERNO FEDERAL
    print("🔗 Acessando o portal de login GOV.BR...")
    driver.get("https://acesso.gov.br")  # Ajuste para a URL de login do Comprasnet/ETP se necessário
    
    # 2. INSERE O CPF
    print("👤 Digitando o CPF...")
    # Substitua pelo ID/Name correto do campo de CPF do site
    campo_cpf = wait.until(EC.presence_of_element_located((By.ID, "accountId")))
    campo_cpf.send_keys(CPF_FIXO)
    
    # Clica no botão avançar/continuar do CPF
    botao_continuar = driver.find_element(By.ID, "botao-avancar") 
    botao_continuar.click()
    
    # 3. INSERE A SENHA
    print("🔑 Digitando a senha...")
    # Substitua pelo ID/Name correto do campo de senha do site
    campo_senha = wait.until(EC.presence_of_element_located((By.ID, "password")))
    campo_senha.send_keys(SENHA_FIXA)
    
    # Clica no botão de entrar/logar
    botao_entrar = driver.find_element(By.ID, "submit-button")
    botao_entrar.click()
    
    print("✅ Login efetuado com sucesso!")
    time.sleep(3)
    
    # 4. NAVEGA ATÉ A ÁREA DE CRIAÇÃO DO ETP DIGITAL
    print("📁 Abrindo o formulário do ETP Digital...")
    # driver.get("URL_DIRETA_DO_FORMULARIO_DE_NOVO_ETP")
    
    # 5. PREENCHE O CAMPO DO OBJETO COM O TEXTO VINDO DO CELULAR
    print("📝 Preenchendo a descrição do objeto...")
    # Substitua pelo ID/Name real do campo de texto do objeto do ETP no site do governo
    campo_objeto_site = wait.until(EC.presence_of_element_located((By.ID, "campo-objeto-etp")))
    campo_objeto_site.send_keys(objeto_etp)
    
    # 6. EXECUTAR AS OUTRAS ETAPAS DO SEU ROBÔ ORIGINAL
    # (Copie aqui as suas linhas de cliques e preenchimentos do seu código original)
    
    print("💾 Salvando o documento...")
    # driver.find_element(By.ID, "botao-salvar-etp").click()
    
    print("🎉 Operação realizada com sucesso total!")

except Exception as e:
    print(f"❌ Ocorreu uma falha durante a execução do robô: {e}")

finally:
    # Fecha o navegador de forma segura nos servidores da nuvem
    driver.quit()
    print("🔌 Conexão encerrada com o servidor.")
