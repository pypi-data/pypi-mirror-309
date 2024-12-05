use super::PlanePartition;

pub fn complement(matrix: &PlanePartition) -> PlanePartition {
    let len = matrix.len;

    let mut complement = PlanePartition {
        len,
        data: vec![vec![len as u8; len]; len],
    };

    for i in (0..len).rev() {
        for j in (0..len).rev() {
            complement[i][j] = complement[i][j] - matrix[len - 1 - i][len - 1 - j];
        }
    }

    complement
}
