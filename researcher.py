import click 
#CLI
import functions

#subcommands
@click.group()
def main():
   pass

#Header extraction
@main.command()
@click.argument('input', type = click.Path())
@click.argument('output', type = click.Path())
@click.option(
    '--nometa', is_flag=True,
    help='extract header without meta-information lines',
)
def header(input, output, nometa):
    try:
        meta, column_names, header_index = functions.get_header(input, ())
        if input == output: 
            try:
                click.confirm('You want to overwrite an input file. Do you want to continue?', abort = True)
            except:
                click.echo('Overwrite is aborted')

        functions.write_vcf(output, meta, column_names, nometa)
    except:
        click.echo("Input file was not found. Try again!")
        quit()

#VCF Filter
@main.command()
@click.argument('input', type = click.Path())
@click.argument('output', type = click.Path())
@click.option(
    '--samples', '-s', multiple = True,
    help='extract only specific sample columns, while others will be omitted'
)
#@click.option(
#    '--samples-file', '-sf', 'samples_file', type = click.Path(),
#    help='extract only specific sample columns, while others will be omitted'
#)
@click.option(
    '--keywords', '-k', multiple = True, type = str,
    help='extract lines with specific keyword'
)
#@click.option(
#    '--keywords-file', '-kf', 'keywords_file', type = click.Path(),
#    help='extract lines with specific keyword'
#)

@click.option(
    '--FILTER', '-f', 'passfail', type = click.Choice(['PASS', 'FAIL'], case_sensitive = False),
    help='extract lines with PASS or FAIL in "FILTER" field'
)
@click.option(
    '--CHROM', '-c', 'chrom', type = str,
    help='extract variants in the range of specific chromosomes'
)
@click.option(
    '--POS', '-p', 'pos', type = str,
    help='extract variants in the range of specific positions'
)
@click.option(
    '--nometa', is_flag=True,
    help='extract header without meta-information lines',
)
def filter(input, output, samples, keywords, passfail, chrom, pos, nometa):
    try:
        #header
        meta, column_names, header_index = functions.get_header(input, samples)
        if input == output: 
            try:
                click.confirm('You want to overwrite an input file. Do you want to continue?', abort = True)
            except:
                click.echo('Overwrite is aborted')
        
        #main df
        df = functions.read_vcf(input, header_index, column_names)
        #if df is empty -> raise Error -> quit()

        #Write header
        functions.write_vcf(output, meta, column_names, nometa)
        #Apply filters and write main df
        functions.get_filter(df, output, samples, keywords, passfail, chrom, pos)
    except ValueError:
        click.echo("Invalid range. Try again!")
        quit()
    except:
        click.echo("Input file was not found. Try again!")
        quit()

#Genotype conversion
@main.command()
@click.argument('input', type = click.Path())
@click.argument('output', type = click.Path())
@click.argument('multiallelic_output', type = click.Path())
@click.option(
    '--nometa', is_flag=True,
    help='extract header without meta-information lines',
)
def gt(input, output, nometa, multiallelic_output):
    meta, column_names, header_index = functions.get_header(input, ())
    arr, multi = functions.number_gt_to_letter_gt(input, column_names)
    functions.write_vcf(output, meta, column_names, nometa, arr)
    functions.write_multi(multiallelic_output, column_names, multi)

##################
################## 
if __name__ == "__main__":
    main()
