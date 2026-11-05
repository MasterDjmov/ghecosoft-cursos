// Sugerencias del editor en las Herramientas (D120): palabras de cada lenguaje, estructuras que se completan solas
// (con Tab se salta al próximo hueco) y las palabras que ya están escritas en el programa. En las clases y las
// micro-misiones no se usan: ahí se aprende a escribirlas.
import { acceptCompletion, autocompletion, completeAnyWord, completeFromList, ifNotIn, snippetCompletion } from '@codemirror/autocomplete';
import { Prec } from '@codemirror/state';
import { keymap } from '@codemirror/view';

const NOT_IN = ['String', 'FormatString', 'StringLiteral', 'RawString', 'Comment', 'LineComment', 'BlockComment', 'TemplateString', 'CharLiteral'];

const words = (type, text) => text.trim().split(/\s+/).map((label) => ({ label, type }));
const snippets = (list) => list.map(([label, detail, template]) => snippetCompletion(template, { label, detail, type: 'keyword', boost: 2 }));

const C_LIKE = [['if', 'si…', 'if (${condicion}) {\n    ${}\n}'], ['else', 'si no…', 'else {\n    ${}\n}'], ['while', 'mientras…', 'while (${condicion}) {\n    ${}\n}']];
const C_FOR = ['for', 'repetir n veces', 'for (int ${i} = 0; ${i} < ${n}; ${i}++) {\n    ${}\n}'];
const C_TYPES = 'int char float double long short unsigned void const struct return break continue switch case default sizeof';

const LISTS = {
    python: [
        ...snippets([
            ['for', 'repetir n veces', 'for ${i} in range(${n}):\n    ${}'],
            ['forin', 'recorrer una lista', 'for ${cosa} in ${lista}:\n    ${}'],
            ['if', 'si…', 'if ${condicion}:\n    ${}'],
            ['ifelse', 'si… si no…', 'if ${condicion}:\n    ${}\nelse:\n    '],
            ['while', 'mientras…', 'while ${condicion}:\n    ${}'],
            ['def', 'una función', 'def ${nombre}(${}):\n    '],
            ['class', 'una clase', 'class ${Nombre}:\n    def __init__(self${}):\n        '],
            ['try', 'atajar un error', 'try:\n    ${}\nexcept ${ValueError}:\n    '],
            ['print', 'mostrar', 'print(${})'],
            ['input', 'preguntar', 'input("${}")'],
        ]),
        ...words('function', 'len range int float str bool list dict set tuple sum min max abs round sorted reversed enumerate zip map filter open type isinstance'),
        ...words('method', 'append insert pop remove sort split join strip upper lower replace keys values items get format'),
    ],
    c: [
        ...snippets([
            ['main', 'el programa', '#include <stdio.h>\n\nint main(void) {\n    ${}\n    return 0;\n}'],
            C_FOR, ...C_LIKE,
            ['printf', 'mostrar', 'printf("${}\\n");'],
            ['scanf', 'leer un entero', 'scanf("%d", &${variable});'],
            ['include', 'una biblioteca', '#include <${stdio.h}>'],
        ]),
        ...words('keyword', C_TYPES),
        ...words('function', 'strlen strcpy strcmp strcat malloc calloc realloc free fopen fclose fgets fprintf fscanf sqrt pow abs rand srand'),
    ],
    cpp: [
        ...snippets([
            ['main', 'el programa', '#include <iostream>\nusing namespace std;\n\nint main() {\n    ${}\n    return 0;\n}'],
            C_FOR, ...C_LIKE,
            ['forin', 'recorrer una colección', 'for (const auto& ${cosa} : ${lista}) {\n    ${}\n}'],
            ['cout', 'mostrar', 'cout << ${} << endl;'],
            ['cin', 'leer', 'cin >> ${variable};'],
            ['class', 'una clase', 'class ${Nombre} {\npublic:\n    ${}\n};'],
            ['include', 'una biblioteca', '#include <${iostream}>'],
        ]),
        ...words('keyword', `${C_TYPES} bool auto class public private protected virtual override new delete nullptr this template typename namespace using true false`),
        ...words('type', 'string vector map set pair unique_ptr shared_ptr'),
        ...words('method', 'push_back pop_back size empty begin end at find insert erase'),
    ],
    java: [
        ...snippets([
            ['main', 'el método principal', 'public static void main(String[] args) {\n    ${}\n}'],
            ['sout', 'mostrar', 'System.out.println(${});'],
            ['scanner', 'leer del teclado', 'Scanner ${entrada} = new Scanner(System.in);'],
            C_FOR, ...C_LIKE,
            ['forin', 'recorrer una colección', 'for (${String} ${cosa} : ${lista}) {\n    ${}\n}'],
            ['class', 'una clase', 'public class ${Nombre} {\n    ${}\n}'],
        ]),
        ...words('keyword', 'public private protected static final abstract class interface extends implements new this super return void int long double float boolean char byte short true false null try catch finally throw throws import package'),
        ...words('type', 'String Integer Double Boolean ArrayList List HashMap Map Scanner Math Object'),
        ...words('method', 'length size add get set remove contains equals toString nextLine nextInt println printf'),
    ],
    csharp: [
        ...snippets([
            ['main', 'el método principal', 'static void Main()\n{\n    ${}\n}'],
            ['cw', 'mostrar', 'Console.WriteLine(${});'],
            ['cr', 'leer', 'Console.ReadLine()'],
            ['for', 'repetir n veces', 'for (int ${i} = 0; ${i} < ${n}; ${i}++)\n{\n    ${}\n}'],
            ['foreach', 'recorrer una colección', 'foreach (var ${cosa} in ${lista})\n{\n    ${}\n}'],
            ['if', 'si…', 'if (${condicion})\n{\n    ${}\n}'],
            ['while', 'mientras…', 'while (${condicion})\n{\n    ${}\n}'],
            ['class', 'una clase', 'class ${Nombre}\n{\n    ${}\n}'],
        ]),
        ...words('keyword', 'using namespace public private protected static void class struct interface new this base return int long double float decimal bool char string var true false null try catch finally throw get set'),
        ...words('type', 'Console Math List Dictionary String Convert File'),
        ...words('method', 'WriteLine Write ReadLine Parse ToString Add Remove Count Length Contains'),
    ],
    php: [
        ...snippets([
            ['echo', 'mostrar', 'echo ${};'],
            ['foreach', 'recorrer un arreglo', 'foreach ($${lista} as $${cosa}) {\n    ${}\n}'],
            ['for', 'repetir n veces', 'for ($${i} = 0; $${i} < ${n}; $${i}++) {\n    ${}\n}'],
            ['if', 'si…', 'if (${condicion}) {\n    ${}\n}'],
            ['while', 'mientras…', 'while (${condicion}) {\n    ${}\n}'],
            ['function', 'una función', 'function ${nombre}(${}) {\n    \n}'],
            ['class', 'una clase', 'class ${Nombre}\n{\n    ${}\n}'],
        ]),
        ...words('function', 'count strlen implode explode array_map array_filter array_keys array_values array_push in_array isset empty var_dump print_r str_replace strtoupper strtolower trim round json_encode json_decode file_put_contents file_get_contents'),
        ...words('keyword', 'return public private protected static new null true false try catch throw namespace use'),
    ],
    javascript: [
        ...snippets([
            ['log', 'mostrar', 'console.log(${});'],
            ['for', 'repetir n veces', 'for (let ${i} = 0; ${i} < ${n}; ${i}++) {\n    ${}\n}'],
            ['forof', 'recorrer una lista', 'for (const ${cosa} of ${lista}) {\n    ${}\n}'],
            ['if', 'si…', 'if (${condicion}) {\n    ${}\n}'],
            ['fn', 'una función flecha', 'const ${nombre} = (${}) => {\n    \n};'],
            ['fetch', 'pedirle algo al Puerto', "const ${respuesta} = await fetch('${/puerto/hola}');\nconst ${datos} = await ${respuesta}.json();"],
            ['click', 'cuando tocan un botón', "document.querySelector('${#boton}').addEventListener('click', () => {\n    ${}\n});"],
        ]),
        ...words('method', 'querySelector querySelectorAll addEventListener setTimeout setInterval clearInterval requestAnimationFrame map filter reduce forEach push includes join split'),
    ],
    asm: [
        ...snippets([
            ['programa', 'el esqueleto', '.model small\n.stack 100h\n.data\n    ${}\n.code\nmain proc\n    mov ax, @data\n    mov ds, ax\n\n    \n\nfin:\n    mov ax, 4C00h\n    int 21h\nmain endp\nend main'],
            ['mostrar', 'INT 21h: un texto', 'mov dx, offset ${texto}\nmov ah, 09h\nint 21h'],
            ['proc', 'un procedimiento', '${nombre} proc\n    ${}\n    ret\n${nombre} endp'],
        ]),
        ...words('keyword', 'mov add sub inc dec mul div cmp jmp je jne jg jl jge jle loop push pop call ret and or xor not shl shr int lea nop xchg neg'),
        ...words('variable', 'ax bx cx dx si di bp sp al ah bl bh cl ch dl dh ds es ss cs'),
        ...words('type', 'db dw dup offset ptr byte word equ'),
    ],
};

/** La lista del lenguaje, más las palabras que ya están en el programa (sin repetir las de la lista). */
function withWordsOfProgram(list) {
    const fromList = completeFromList(list);
    const labels = new Set(list.map((item) => item.label));

    return async (context) => {
        const [listed, written] = await Promise.all([fromList(context), completeAnyWord(context)]);
        if (!listed || !written) return listed ?? written;

        return { ...listed, options: [...listed.options, ...written.options.filter((option) => !labels.has(option.label))] };
    };
}

export function editorCompletions(language) {
    const list = LISTS[language];

    return [
        // Las que traen HTML, CSS y SQL ya alcanzan; en el resto, esta lista reemplaza a la del lenguaje para no repetirlas.
        list ? autocompletion({ override: [ifNotIn(NOT_IN, withWordsOfProgram(list))] }) : [],
        Prec.high(keymap.of([{ key: 'Tab', run: acceptCompletion }])),
    ];
}
