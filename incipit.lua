function gabc_to_incipit(gabc)
  local incipit_end_index = string.find(gabc, "<sp>*</sp>", 1, true)
  local euouae_start_index = string.find(gabc, "<eu>", 1, true) + string.len("<eu>")
  
  local incipit = string.sub(gabc, 1, incipit_end_index-1)
  local euouae = string.sub(gabc, euouae_start_index-4, -1)
  local reversed_incipit = string.reverse(incipit)
  local incipit_last_paren_index = string.find(reversed_incipit, "(", 1, true)
  local char_before_last_paren = string.sub(reversed_incipit, incipit_last_paren_index+1, incipit_last_paren_index+1)
  if char_before_last_paren == "," or char_before_last_paren == ";" or char_before_last_paren == ":"
  then
    reversed_incipit = string.sub(reversed_incipit, 1, incipit_last_paren_index).."."..string.sub(reversed_incipit, incipit_last_paren_index+2, -1)
  else
    reversed_incipit = string.sub(reversed_incipit, 1, incipit_last_paren_index).."."..string.sub(reversed_incipit, incipit_last_paren_index+1, -1)
  end
  incipit = string.reverse(reversed_incipit)
  local result = incipit.."(::) "..euouae
  return result
end

local mystr = "(c4) A(g|vi)vér(f|ta)ta(h|vi) Dó(j|vihg)mi(j|vihh)nus(i|vi) <sp>*</sp>(,) cap(g|ta)ti(i|vi)vi(j|vihh)tá(h|vi)tem(h|vi) ple(i|vihh)bis(h|vi) su(g.|ta)æ.(g.|ta) (::) <eu>E(j) U(j) O(i) U(j) A(h) E.(g) </eu>(::)"

result = gabc_to_incipit(mystr)

print(result)