const jsdom = require('jsdom');
const vm = require('vm');

function solve(url, html) {

    const dom = new jsdom.JSDOM(html, {
        url,
        runScripts: 'outside-only',
    });

    const { document } = dom.window;
    const script = document.querySelector('script');
    const form = document.getElementById('challenge-form');

    const re = new RegExp(`
      setTimeout\\(function\\(\\){
        (?<innerScript>(.|\\n)*)
        f.submit\\(\\);
      },.*4000\\);`, 'm');

    const m = re.exec(script.text);
    if (m == null) {
        console.log(script.text);
        throw 'bad script';
    }
    const { innerScript } = m.groups;

    const vmScript = new vm.Script(innerScript);
    dom.runVMScript(vmScript);

    var data = {};
    for (var i = 0; i < form.elements.length; i++) {
        const { name, value } = form.elements[i];
        data[name] = value;
    }

    return {
        url: form.action,
        data,
    };
}

module.exports = solve;
