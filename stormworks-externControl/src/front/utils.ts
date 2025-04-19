export function parseBool(value : any) : boolean {
    if(value === undefined){
        return false;
    }
    value = value.toString().toLowerCase();
    if(value === 'true' || value === true){
        return true;
    }else if(value === 'false' || value === false){
        return false;
    }
    throw new Error('Invalid boolean value "' + value + '"');
}


export function getCurrentLayout(_window : Window) : string {
    let url = new URL(_window.location.href);
    let filename = url.pathname.split('/').pop();
    if(filename === undefined){
        throw new Error('Invalid URL; cannot determine layout');
    }
    filename = filename.split('.')[0];
    if(filename === '' || filename === undefined){
        throw new Error('Invalid URL; cannot determine layout');
    }
    return filename;
}


export function strip(value : string|undefined) : string {
    if(value === undefined){
        return '';
    }
    return value.replace(/^\s+|\s+$/g, '');
}

export function clamp(value : number, min : number, max : number) : number {
    return Math.min(Math.max(value, min), max);
}

export function scale(value : number, min : number, max : number, newMin : number, newMax : number) : number {
    return (value - min) / (max - min) * (newMax - newMin) + newMin;
}

export function parseInputMode(value : string) : {mode: string, channel: string} {
    // none | input:{channel} | output:{channel}
    // channel is {b|n}{1-32}
    let tokens = value.split(':');
    let mode = tokens[0];
    let channel = tokens[1];
    if(mode === 'none'){
        return {mode: 'none', channel: ''};
    }

    if(channel === undefined){
        throw new Error('Invalid input mode "' + value + '"');
    }

    if(mode === 'input'){
        return {mode: 'input', channel: channel};
    }
    if(mode === 'output'){
        return {mode: 'output', channel: channel};
    }
    throw new Error('Invalid input mode "' + value + '"');
}