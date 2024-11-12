from src.models.domain_model import Domain, DomainSerializer


def read_domain(domain_id) -> dict:
    """Retorna os dados do domínio com o id passado.

    Returns:
        dict: dados do dominio

    Raises:
        ObjectDoesNotExist: se o dominio não existir
        ValueError: se o id for inválido
    """
    domain = Domain.objects.get(id=domain_id)
    return DomainSerializer(domain).data
