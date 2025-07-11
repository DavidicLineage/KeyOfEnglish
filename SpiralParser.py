import json

class GrammarLoader:
    def __init__(self, grammar_file):
        with open(grammar_file, 'r', encoding='utf-8') as f:
            self.grammar_data = json.load(f)

    def load(self, glyph_set):
        return self.grammar_data.get(glyph_set, {})

class GlyphResolver:
    def __init__(self, glyph_data):
        self.glyph_data = glyph_data

    def resolve(self, glyph):
        return next((g for g in self.glyph_data if g['glyph'] == glyph), {
            'glyph': glyph,
            'DAM': {
                'layer_1': '',
                'layer_2': '',
                'layer_3': ''
            }
        })

class ParserCore:
    def __init__(self, grammar):
        self.grammar = grammar

    def parse(self, glyph_sequence, resolver):
        n = len(glyph_sequence)
        pairs = []

        if n == 0:
            return []

        # Generate canonical spiral index pairs
        if n % 2 == 1:
            center = n // 2
            pairs.append([center])
            step = 1
            while center - step >= 0 and center + step < n:
                pairs.append([0 + step - 1, n - step])  # outermost
                pairs.append([center - step, center + step])  # inner
                step += 1
        else:
            left = n // 2 - 1
            right = n // 2
            pairs.append([left, right])
            step = 1
            while left - step >= 0 and right + step < n:
                pairs.append([0 + step - 1, n - step])  # outermost
                pairs.append([left - step, right + step])  # inner
                step += 1

        ordered_glyphs = []

        for role_counter, group in enumerate(pairs, start=1):
            for index in group:
                if 0 <= index < n:
                    glyph = glyph_sequence[index]
                    resolved = resolver.resolve(glyph)
                    ordered_glyphs.append({
                        'position': role_counter,
                        'glyph': glyph,
                        'original_index': index + 1,
                        'role': f"spiral_{role_counter}",
                        'DAM': resolved.get('DAM', {})
                    })

        return ordered_glyphs

class ExecutionMapper:
    def __init__(self, grammar):
        self.grammar = grammar

    def map(self, glyph_sequence):
        return list(glyph_sequence) if self.grammar.get('execution_order') == 'left_to_right' else list(reversed(glyph_sequence))

def parse_input(glyph_sequence, glyph_set, grammar_file, glyph_data_file):
    grammar_loader = GrammarLoader(grammar_file)
    grammar = grammar_loader.load(glyph_set)

    with open(glyph_data_file, 'r', encoding='utf-8') as f:
        glyph_data = json.load(f)

    resolver = GlyphResolver(glyph_data)
    parser = ParserCore(grammar)
    mapper = ExecutionMapper(grammar)

    parsed_stack = parser.parse(glyph_sequence, resolver)
    execution_sequence = mapper.map(glyph_sequence)

    return {
        'parsed_stack': parsed_stack,
        'execution_sequence': execution_sequence,
        'source': glyph_sequence,
        'glyph_set': glyph_set
    }

# Example Usage
if __name__ == "__main__":
    result = parse_input("LOGOS", "English", "grammar_registry.json", "glyphs_english_unified_dam.json")
    print(json.dumps(result, indent=2))
