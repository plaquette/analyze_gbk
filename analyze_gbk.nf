#!/usr/bin/env nextflow
nextflow.enable.dsl=2


process compute_csv{

    label 'q_mini'
    
    input:
    tuple path(inputFile), val(percentage)

    output:
    path("out/*.csv", emit: csv_single)

    script:
    """
    mkdir -p out

    python3 $baseDir/scr/access_quality.py ${inputFile} ${percentage} out/

    """
}


process publish_csv{

    publishDir params.out,
    mode : 'copy',
    pattern : "${params.run}/gbk_metric.csv"
    
    input:
    path(csv)

    output:
    path("${params.run}/gbk_metric.csv", emit: csv)
    
    script:
    """
    mkdir -p ${params.run}
    cp gbk_metric.csv ${params.run}
    """
}



workflow analyze_gbk{

    take: data
    
    main:

        percentage_ch = Channel.value(data.percentage)

        input_ch = Channel.fromPath(data.input + "/*.gbk")   

        comb_in = input_ch.combine(percentage_ch)

        compute_csv(comb_in)

        csv_ch = compute_csv.out.collectFile(name: 'gbk_metric.csv', newLine: false, keepHeader: true, skip: 1)

        publish_csv(csv_ch)

    

}

workflow{
    
    params.run = 'test'

    params.in = "$baseDir/example_data"

    params.out = "$baseDir/out/"

    params.percentage = 0.95

    data = [input: params.in, run: params.run, out: params.out, percentage: params.percentage]
    main:
        analyze_gbk(data)
        
}
