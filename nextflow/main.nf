nextflow.enable.dsl=2

// Importar módulos
include { analyze } from './modules/analyze.nf'
include { clean }   from './modules/clean.nf'
include { reports } from './modules/reports.nf'

// Definir parámetros
//params.input_file = "data/input.txt"
//params.output_dir = "data/output"

workflow {
    input_file = file(params.input_file)
    output_dir = file(params.output_dir)

    analyze(input_file, output_dir)
    clean(input_file, output_dir)
    reports(input_file, output_dir)
}