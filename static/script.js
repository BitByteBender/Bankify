function obfuscate_id(user_id) {
    let obfuscated = Array.from(user_id).reverse().map(c => String.fromCharCode(c.charCodeAt(0) + 3)).join('');
    return obfuscated;
}
