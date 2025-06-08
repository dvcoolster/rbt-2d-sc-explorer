#!/usr/bin/env bash
# run_qe_docker.sh – launch QE SCF + PH for each strain_*pc folder using Docker
# Requires: Docker installed, internet to pull ghcr.io/qe-lab/espresso:7.2 image

set -e
IMAGE="ghcr.io/qe-lab/espresso:7.2"

echo "Pulling QE image ${IMAGE} (if not present) …"
docker pull "${IMAGE}"

echo "Launching calculations …"
for d in strain_*pc; do
  echo "=== $d ==="
  docker run --rm -v "$(pwd)/$d:/calc" -w /calc "${IMAGE}" pw.x < scf.in > scf.out
  docker run --rm -v "$(pwd)/$d:/calc" -w /calc "${IMAGE}" ph.x < ph.in > ph.out || true
  echo "   outputs: $d/scf.out  $d/ph.out"
  echo "-------------"
done

echo "All Docker runs finished." 