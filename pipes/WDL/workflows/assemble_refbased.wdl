import "../tasks/tasks_assembly.wdl" as assembly
import "../tasks/tasks_reports.wdl" as reports

workflow assemble_refbased {

  File     reference_fasta
  File     reads_unmapped_bam
  File?    novocraft_license
  Boolean? skip_mark_dupes=false

  call reports.plot_coverage as align_to_ref {
    input:
        assembly_fasta     = reference_fasta,
        reads_unmapped_bam = reads_unmapped_bam,
        novocraft_license  = novocraft_license,
        skip_mark_dupes    = skip_mark_dupes,
        aligner            = "bwa",
        aligner_options    = "-k 12 -B 1"  ## alternatively for novoalign: "-r Random -l 40 -g 40 -x 20 -t 501 -k"
  }

  call assembly.ivar_trim {
    input:
        aligned_bam = align_to_ref.aligned_only_reads_bam
  }

  call assembly.refine_assembly_with_aligned_reads as call_consensus {
    input:
        reference_fasta   = reference_fasta,
        reads_aligned_bam = ivar_trim.aligned_trimmed_bam,
        novocraft_license  = novocraft_license
  }

  call reports.plot_coverage as align_to_self {
    input:
        assembly_fasta     = call_consensus.refined_assembly_fasta,
        reads_unmapped_bam = reads_unmapped_bam,
        novocraft_license  = novocraft_license,
        skip_mark_dupes    = skip_mark_dupes,
        aligner            = "bwa"
  }

}
