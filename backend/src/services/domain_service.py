from src.models.domain_model import Domain, DomainSerializer


def read_domain(domain_id) -> dict:
    """Retorna os dados do usuário com o id passado.
    Params:
        domain_id: id do dominio

    Returns:
        dict: dados do dominio

    Raises:
        ObjectDoesNotExist: se o dominio não existir
        ValueError: se o id for inválido
    """
    domain = Domain.objects.get(id=domain_id)
    return DomainSerializer(domain).data
