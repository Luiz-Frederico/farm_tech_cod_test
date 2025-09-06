import math
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional, Dict, Any

# --- Modelagem dos Dados (Classes e Estruturas) ---

@dataclass
class Insumo:
    """Representa um insumo agrícola com nome e quantidade em litros."""
    produto: str
    litros: float

    def __str__(self) -> str:
        return f"{self.produto} - {self.litros:.2f} L"

class Cultura(ABC):
    """
    Classe Abstrata Base para representar uma cultura.
    Define a interface comum que todas as culturas devem seguir (Polimorfismo).
    """
    def __init__(self, nome: str):
        self.nome = nome
        self.insumo: Optional[Insumo] = None

    @abstractmethod
    def calcular_area(self) -> float:
        """Método abstrato para calcular a área da plantação."""
        pass

    @abstractmethod
    def obter_detalhes(self) -> Dict[str, Any]:
        """Método abstrato para retornar os detalhes específicos da cultura."""
        pass

    @abstractmethod
    def calcular_metros_lineares_para_insumos(self) -> float:
        """Calcula o total de metros lineares para aplicação de insumos."""
        pass

    def __str__(self) -> str:
        detalhes = ', '.join(f"{k}: {v}" for k, v in self.obter_detalhes().items())
        info_insumo = f"Insumo: {self.insumo}" if self.insumo else "Insumo: Não calculado"
        return (
            f"Cultura: {self.nome.capitalize()} | "
            f"Área: {self.calcular_area():.2f} m² | "
            f"Detalhes: ({detalhes}) | "
            f"{info_insumo}"
        )

class Cafe(Cultura):
    """Representa uma plantação de Café com área retangular."""
    def __init__(self, comprimento: float, largura: float):
        super().__init__("café")
        self.comprimento = comprimento
        self.largura = largura

    def calcular_area(self) -> float:
        return self.comprimento * self.largura

    def obter_detalhes(self) -> Dict[str, Any]:
        return {"comprimento": self.comprimento, "largura": self.largura}

    def calcular_metros_lineares_para_insumos(self) -> float:
        # A lógica original dependia de "ruas", que é uma entrada externa ao objeto.
        # Assumindo que o cálculo de insumos será feito para a área total.
        # Vamos manter a lógica de pedir o número de ruas no momento do cálculo.
        return self.comprimento

class Milho(Cultura):
    """Representa uma plantação de Milho com área circular (pivô central)."""
    def __init__(self, raio: float):
        super().__init__("milho")
        self.raio = raio

    def calcular_area(self) -> float:
        return math.pi * (self.raio ** 2)

    def obter_detalhes(self) -> Dict[str, Any]:
        return {"raio": self.raio}
    
    def calcular_metros_lineares_para_insumos(self) -> float:
        # A lógica original era 'raio * 2 * math.pi', que é o perímetro.
        # Vamos usar essa base para o cálculo.
        return 2 * math.pi * self.raio


# --- Lógica de Negócio (Gerenciamento) ---

class GerenciadorPlantacoes:
    """
    Classe responsável por gerenciar todas as operações de CRUD 
    para as plantações.
    """
    def __init__(self):
        self._plantacoes: List[Cultura] = []

    def adicionar_plantacao(self, cultura: Cultura):
        self._plantacoes.append(cultura)
        print("\n> Plantação adicionada com sucesso!")

    def listar_plantacoes(self):
        if not self._plantacoes:
            print("\n> Nenhuma plantação cadastrada.")
            return

        print("\n--- Lista de Plantações ---")
        for i, cultura in enumerate(self._plantacoes):
            print(f"Índice {i}: {cultura}")
    
    def obter_plantacao(self, indice: int) -> Optional[Cultura]:
        if 0 <= indice < len(self._plantacoes):
            return self._plantacoes[indice]
        return None

    def remover_plantacao(self, indice: int) -> bool:
        plantacao = self.obter_plantacao(indice)
        if plantacao:
            self._plantacoes.pop(indice)
            print(f"\n> Plantação no índice {indice} removida com sucesso!")
            return True
        print("\n> Índice inválido.")
        return False

# --- Interface com o Usuário (UI) ---

class Menu:
    """
    Gerencia a interação com o usuário, exibindo o menu e coletando as entradas.
    """
    def __init__(self):
        self._gerenciador = GerenciadorPlantacoes()
        self._opcoes = {
            '1': ('Adicionar Plantação', self._adicionar_plantacao),
            '2': ('Listar Plantações', self._listar_plantacoes),
            '3': ('Atualizar Plantação', self._atualizar_plantacao),
            '4': ('Deletar Plantação', self._deletar_plantacao),
            '5': ('Calcular Insumos para Plantação', self._calcular_insumos),
            '6': ('Sair', self._sair)
        }

    def _obter_input_numerico(self, prompt: str) -> float:
        """Laço para garantir que o input do usuário seja um número válido."""
        while True:
            try:
                return float(input(prompt))
            except ValueError:
                print("> Entrada inválida. Por favor, digite um número.")

    def _selecionar_cultura_para_criar(self) -> Optional[Cultura]:
        """Coleta os dados para criar um novo objeto de Cultura."""
        tipo_cultura = input("Digite o tipo de cultura (cafe ou milho): ").lower()
        if tipo_cultura == "cafe":
            comprimento = self._obter_input_numerico("Digite o comprimento (m): ")
            largura = self._obter_input_numerico("Digite a largura (m): ")
            return Cafe(comprimento, largura)
        elif tipo_cultura == "milho":
            raio = self._obter_input_numerico("Digite o raio do pivô (m): ")
            return Milho(raio)
        else:
            print("\n> Cultura inválida. Tente novamente.")
            return None

    def _adicionar_plantacao(self):
        print("\n--- Adicionar Nova Plantação ---")
        nova_cultura = self._selecionar_cultura_para_criar()
        if nova_cultura:
            self._gerenciador.adicionar_plantacao(nova_cultura)

    def _listar_plantacoes(self):
        self._gerenciador.listar_plantacoes()
        
    def _selecionar_indice(self) -> Optional[int]:
        """Pede ao usuário para selecionar um índice e o valida."""
        if not self._gerenciador._plantacoes:
             print("\n> Nenhuma plantação cadastrada para selecionar.")
             return None
        
        self._listar_plantacoes()
        try:
            indice = int(input("\nDigite o índice desejado: "))
            if self._gerenciador.obter_plantacao(indice) is not None:
                return indice
            else:
                print("> Índice inválido.")
                return None
        except ValueError:
            print("> Entrada inválida. Digite um número inteiro.")
            return None

    def _atualizar_plantacao(self):
        print("\n--- Atualizar Plantação ---")
        indice = self._selecionar_indice()
        if indice is not None:
            print(f"\nAtualizando dados para o índice {indice}. Por favor, insira os novos valores.")
            cultura_atualizada = self._selecionar_cultura_para_criar()
            if cultura_atualizada:
                # Substitui o objeto antigo pelo novo
                self._gerenciador._plantacoes[indice] = cultura_atualizada
                print(f"\n> Plantação no índice {indice} atualizada com sucesso!")

    def _deletar_plantacao(self):
        print("\n--- Deletar Plantação ---")
        indice = self._selecionar_indice()
        if indice is not None:
            self._gerenciador.remover_plantacao(indice)

    def _calcular_insumos(self):
        print("\n--- Cálculo de Insumos ---")
        indice = self._selecionar_indice()
        if indice is not None:
            cultura = self._gerenciador.obter_plantacao(indice)
            
            produto = input("Qual o produto a ser aplicado? ")
            ruas = int(self._obter_input_numerico("Quantas ruas a lavoura tem? "))
            ml_por_metro = self._obter_input_numerico("Quantos mL por metro você deseja aplicar? ")

            # O cálculo agora usa o método polimórfico da classe
            base_metros = cultura.calcular_metros_lineares_para_insumos()
            total_metros = base_metros * ruas
            
            litros_necessarios = (total_metros * ml_por_metro) / 1000
            
            # Atualiza o objeto com a informação do insumo
            cultura.insumo = Insumo(produto, litros_necessarios)
            
            print(f"\n> Para a cultura de {cultura.nome}, serão necessários {litros_necessarios:.2f} litros de {produto}.")
            print("> Informação de insumo salva na plantação.")

    def _sair(self):
        print("\nObrigado por usar a FarmTech Solutions. Até mais!")
        return True # Sinaliza para o loop principal terminar

    def exibir(self):
        """Exibe o menu principal e gerencia o loop da aplicação."""
        deve_sair = False
        while not deve_sair:
            print("\n" + "="*40)
            print("  FarmTech Solutions - Agricultura Digital")
            print("="*40)
            for key, (label, _) in self._opcoes.items():
                print(f"{key}. {label}")
            
            escolha = input("Escolha uma opção: ")
            
            opcao = self._opcoes.get(escolha)
            if opcao:
                # A função de saída retorna True para quebrar o loop
                deve_sair = opcao[1]()
            else:
                print("\n> Opção inválida. Tente novamente.")


# --- Ponto de Entrada da Aplicação ---
if __name__ == "__main__":
    app = Menu()
    app.exibir()
