process reports {
    input:
    path input_file
    path output_dir

    output:
    path "${output_dir}/result4.txt"

    script:
    """
    cat $input_file > $output_dir/result4.txt

    python3 ../../../modules/grafico.py reporte.pdf grafico.png
    mv grafico.png $output_dir/grafico.png
    mv reporte.pdf $output_dir/reporte.pdf
    """       
}
