use itertools::Itertools;

use super::PlanePartition;

pub fn find_orbit_length(matrix: &PlanePartition) -> usize {
    let mut curr = rowmotion(&matrix);
    let mut count = 1;
    while curr != *matrix {
        count += 1;
        curr = rowmotion(&curr);
    }
    count
}

pub fn find_orbit(matrix: &PlanePartition) -> Vec<Vec<Vec<u8>>> {
    let mut orbit = vec![];
    orbit.push(matrix.clone().data);
    let mut curr = rowmotion(&matrix);
    while curr != *matrix {
        orbit.push(curr.clone().data);
        curr = rowmotion(&curr);
    }
    orbit
}

pub fn rowmotion(matrix: &PlanePartition) -> PlanePartition {
    let max = matrix.len as u8;
    let len = matrix.len;

    let mut ret = PlanePartition {
        len,
        data: vec![vec![0; len]; len]
    };

    let poss_min_not_in = matrix
        .clone()
        .into_iter()
        .map(|row| row.into_iter().map(|x| (x + 1).clamp(0, max)).collect_vec())
        .collect_vec();

    let min_not_in = poss_min_not_in.into_iter().enumerate().map(|(i, row)| {
        row.into_iter().enumerate().map(move |(j, elem)| {
            let left = if j == 0 { u8::MAX } else { matrix[i][j - 1] };
            let otop = if i == 0 { u8::MAX } else { matrix[i - 1][j] };
            if elem == matrix[i][j] {
                0
            } else if elem <= left && elem <= otop {
                elem
            } else {
                0
            }
        }).collect_vec()
    }).collect_vec();


    for i in (0..len).rev() {
        let mut min = 0;
        for j in (0..len).rev() {
            min = min.max(min_not_in[i][j]);
            ret[i][j] = min;
        }
    }

    for j in (0..len).rev() {
        let mut min = 0;
        for i in (0..len).rev() {
            min = min.max(min_not_in[i][j]).max(ret[i][j]);
            ret[i][j] = min;
        }
    }

    ret
}
