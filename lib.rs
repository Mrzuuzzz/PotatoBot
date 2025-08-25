#!
[
    allow
    (
        unused_variables,
        unused_parens
    )
]

pub
fn mix_quotes(from : &str, into : &str, insertion_seperator : &str) -> String 
{
    let lcs : Vec<char> = lcs(from, into).chars().collect();
    let into : Vec<char> = into.chars().collect::<Vec<char>>();
    
    let mut lcs_idx : usize = 0;
    let mut into_idx : usize = 0;
    let mut ret : String = String::with_capacity(into.len() * 3);

    while (lcs_idx < lcs.len())
    {
        if (lcs[lcs_idx] != into[into_idx])
        {
            ret.push_str(insertion_seperator);
            while
            (
                into_idx < into.len()
                && lcs[lcs_idx] != into[into_idx]
            )
            {
                ret.push(into[into_idx]);
                into_idx += 1;
            }
            if (lcs_idx != lcs.len())
            { ret.push_str(insertion_seperator); }
        }
        while
        (
            lcs_idx < lcs.len()
            && into_idx < into.len()
            && lcs[lcs_idx] == into[into_idx]
        )
        {
            ret.push(lcs[lcs_idx]);
            lcs_idx += 1;
            into_idx += 1;
        }
    }

    //Copy whats left of into into ret
    if (into[into_idx..].len() != 0)
    {
        ret.push_str(insertion_seperator);
        ret.push_str(&into[into_idx..].iter().collect::<String>());
        ret.push_str(insertion_seperator);
    }

    ret
}

//unsure if i want to return String since I immediatly turn it back
//into a Vec<char> but this function returning String just feels right
pub
fn lcs(from : &str, into : &str) -> String
{
    let from : Vec<char> = from.chars().collect::<Vec<char>>();
    let into : Vec<char> = into.chars().collect::<Vec<char>>();

    let mut c_matrix : Vec<Vec<u32>> = vec![vec![0 ; into.len() + 1 ] ; from.len() + 1];

    for i in (1..from.len() + 1)
    {
        let i : usize = i;

        for j in (1..into.len() + 1)
        {
            let j : usize = j;
            
            if (from[i - 1] == into[j - 1])
            { c_matrix[i][j] = c_matrix[i - 1][j - 1] + 1; }
            else
            { c_matrix[i][j] = u32::max(c_matrix[i - 1][j], c_matrix[i][j - 1]); }
        }
    }
    //dbg!(&c_matrix);

    backtrace
    (
        &c_matrix,
        &from,
        &into,
        from.len(),
        into.len()
    )
        .iter()
        .collect::<String>()
}

fn backtrace
(
    c_matrix : &Vec<Vec<u32>>,
    from : &Vec<char>,
    into : &Vec<char>,
    i : usize,
    j : usize
)
-> Vec<char>
{
    if (i == 0 || j == 0)
    { Vec::with_capacity(usize::max(c_matrix.len(), c_matrix[0].len())) }
    else if (from[i - 1] == into[j - 1])
    {
        let mut ret : Vec<char> = 
            backtrace
            (
                c_matrix,
                from,
                into,
                i - 1,
                j - 1
            );

        ret.push(from[i - 1]);
        ret
    }
    else
    {
        let mut i : usize = i;
        let mut j : usize = j;
        if (c_matrix[i][j - 1] < c_matrix[i - 1][j])
        { i -= 1; }
        else
        { j -= 1; }

        backtrace
        (
            c_matrix,
            from,
            into,
            i,
            j
        )
    }
    
}