import click


@click.command()
@click.argument("schema_file", type=click.Path(exists=True))
@click.option(
    "--db-type",
    type=click.Choice(["postgres", "mysql", "sqlite"], case_sensitive=False),
    required=True,
    help="Tipo de banco de dados.",
)
@click.option(
    "--output-dir",
    type=click.Path(),
    default="output",
    help="Diretório para salvar a API gerada.",
)
def generate(schema_file, db_type, output_dir):
    """
    Gera uma API FastAPI baseada no arquivo SQL fornecido.

    \b
    ARGUMENTOS:
    schema_file: Caminho para o arquivo SQL contendo o schema do banco de dados.
    """
    click.echo(f"Arquivo de esquema: {schema_file}")
    click.echo(f"Tipo de banco de dados: {db_type}")
    click.echo(f"Diretório de saída: {output_dir}")


if __name__ == "__main__":
    generate()
