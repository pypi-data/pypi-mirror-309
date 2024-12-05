use std::{collections::BTreeSet, usize};

use itertools::Itertools;

pub mod impls;
pub mod rowmotion;
pub mod complement;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PlanePartition {
    pub len: usize,
    pub data: Vec<Vec<u8>>,
}

#[derive(Debug, Default, Clone)]
pub struct PlanePartitonSet(BTreeSet<(u8, u8, u8)>);

pub fn is_plane_partition(matrix: &PlanePartition) -> bool {
    let len = matrix.len();
    for i in 0..len {
        for j in 0..len-1 {
            if matrix[i][j] < matrix[i][j+1] {
                return false;
            }
        }
    }

    for j in 0..len {
        for i in 0..len-1 {
            if matrix[i][j] < matrix[i+1][j] {
                return false;
            }
        }
    }

    true
}

pub fn check_point_in_matrix(point: (u8, u8, u8), matrix: &PlanePartition) -> bool {
    return matrix[point.0 as usize][point.1 as usize] > point.2;
}

pub fn cardinality(matrix: &PlanePartition) -> usize {
    matrix.clone()
        .into_iter()
        .map(|x| x.into_iter().map(|x| x as usize).collect_vec())
        .flatten()
        .sum::<usize>()
}

pub fn s3_one_point(point: (u8, u8, u8)) -> [(u8, u8, u8); 6] {
    let i = point.0;
    let j = point.1;
    let k = point.2;

    [
        (i, j, k),
        (j, k, i),
        (k, i, j),
        (k, j, i),
        (j, i, k),
        (i, k, j),
    ]
}

pub fn matrix_to_set(matrix: &PlanePartition) -> PlanePartitonSet {
    let mut set = PlanePartitonSet::default();
    let len = matrix.len;

    // We never really use anything more than n=20, and 20^3 = 8000, which really isn't that bad. 
    // 8000 is baby number to big computer.
    for i in 0..len {
        for j in 0..len {
            for k in 0..len {
                set.insert((i as u8, j as u8, k as u8));
            }
        }
    }

    PlanePartitonSet(
        set.into_iter()
            .filter(|x| check_point_in_matrix(*x, &matrix))
            .collect::<BTreeSet<_>>(),
    )
}

pub fn set_to_matrix(set: &PlanePartitonSet, len: usize) -> PlanePartition {
    let mut matrix = PlanePartition {
        len,
        data: vec![vec![0; len]; len],
    };

    for &(i, j, k) in set.iter() {
        matrix[i as usize][j as usize] = u8::max(matrix[i as usize][j as usize], k + 1)
    }

    matrix
}

pub fn ungravity_matrix(matrix: &PlanePartition) -> PlanePartition {
    let mut mat: Vec<Vec<u8>> = vec![];

    // should ungravity the matrix
    for x in 0..matrix.len() {
        let mut vec: Vec<u8> = vec![];
        for y in 0..matrix[0].len() {
            if matrix[y][x] == 0 {
                vec.push(0);
            } else {
                vec.push(matrix[x][y] + x as u8 + y as u8);
            };
        }
        for _ in 0..x {
            vec.insert(0, 0);
            let _ = vec.pop();
        }
        mat.push(vec);
    }

    return PlanePartition {
        len: matrix.len,
        data: mat,
    };
}

pub fn strongly_stable_to_totally_stable(matrix: &PlanePartition) -> PlanePartition {
    let matrix = ungravity_matrix(matrix);

    let points = matrix_to_set(&matrix);

    let mut set_rep = PlanePartitonSet::default();
    for point in points.into_iter() {
        s3_one_point(point).iter().for_each(|x| {
            set_rep.insert(*x);
        });
    }
    set_to_matrix(&set_rep, matrix.len)
}
