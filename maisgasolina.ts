function showValues(ciphertext) {
    let idx = 0
    const plaintext = []
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

    if (!ciphertext) return ciphertext;
    (ciphertext = ciphertext.substring(2)), (ciphertext += "");

    console.debug("Decoding:", ciphertext);
    do {
        const c1 = alphabet.indexOf(ciphertext.charAt(idx++));
        const c2 = alphabet.indexOf(ciphertext.charAt(idx++));
        const c3 = alphabet.indexOf(ciphertext.charAt(idx++));
        const c4 = alphabet.indexOf(ciphertext.charAt(idx++));

        const l = (c1 << 18) | (c2 << 12) | (c3 << 6) | c4;

        const o1 = (l >> 16) & 255;
        const o2 = (l >> 8) & 255;
        const o3 = 255 & l;

        if (64 == c3) {
            plaintext.push(String.fromCharCode(o1))
        } else if (64 == c4) {
            plaintext.push(String.fromCharCode(o1, o2))
        } else {
            plaintext.push(String.fromCharCode(o1, o2, o3))
        }
    } while (idx < ciphertext.length);

    return plaintext.join('').substring(2)
}

console.log(showValues("P0MjQxLjQ5NQ==")); // 1.495
console.log(showValues("pMMjcxLjM5NQ==")); // 1.395
