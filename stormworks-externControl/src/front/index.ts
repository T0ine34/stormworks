import { ToggleButton } from './elements/ToggleButton.js';
import { PushButton } from './elements/PushButton.js';
import { Slider } from './elements/Slider.js';
import { BoolDisplay } from './elements/BoolDisplay.js';
import { RGBDisplay } from './elements/RGBDisplay.js';
import { Keypad } from './elements/Keypad.js';
import { NumberDisplay } from './elements/NumberDisplay.js';
import { RotationSelector } from './elements/RotationSelector.js';
import { parseBool } from './utils.js';

function getName(){
    let name_element = document.querySelector('#name');
    if (name_element === null) {
        throw new Error('Missing name element');
    }
    let name = name_element.textContent;
    if (name === null) {
        throw new Error('Missing name text content');
    }
    name = name.trim();
    if (name === '') {
        throw new Error('Name is empty');
    }
    return name;
}

function parseContainer(container : Element, defaultValues : {[key: string]: string}) {
    for (let i = 0; i < container.children.length; i++) {
        const element = container.children[i];
        if (!(element instanceof HTMLElement)) {
            continue;
        }
        if (element.classList.contains('button')) {
            if (element.getAttribute('data-toggle') === 'true') {
                let channel = element.getAttribute('data-channel');
                if (channel === null) {
                    throw new Error('Missing channel attribute on toggle button');
                }
                new ToggleButton(element, parseBool(defaultValues[channel]));
                if(defaultValues[channel] === 'True'){
                    element.classList.add('active');
                }
            } else {
                new PushButton(element);
            }
        }
        else if (element.classList.contains('slider')) {
            let channel = element.getAttribute('data-channel');
            if (channel === null) {
                throw new Error('Missing channel attribute on slider');
            }
            let value = defaultValues[channel];
            console.log(channel, defaultValues)
            if (value === undefined) {
                throw new Error('Missing default value for slider');
            }
            new Slider(element, parseFloat(value));
        }
        else if (element.classList.contains('mono-color')) {
            new BoolDisplay(element);
        }
        else if (element.classList.contains('rgb-color')) {
            new RGBDisplay(element);
        }
        else if (element.classList.contains('container')) {
            parseContainer(element, defaultValues);
        }
        else if (element.classList.contains('keypad')) {
            let channel = element.getAttribute('data-channel');
            if (channel === null) {
                throw new Error('Missing channel attribute on keypad');
            }
            new Keypad(element, defaultValues[channel]);
        }
        else if (element.classList.contains('number-display')) {
            new NumberDisplay(element);
        }
        else if (element.classList.contains('rotation-selector')) {
            let channel = element.getAttribute('data-channel');
            if (channel === null) {
                throw new Error('Missing channel attribute on rotation selector');
            }
            let value = defaultValues[channel];
            if (value === undefined) {
                throw new Error('Missing default value for rotation selector');
            }
            new RotationSelector(element, parseFloat(value));
            let rotator = element.querySelector('.rotator');
            if (rotator === null) {
                throw new Error('Missing rotator element in rotation selector');
            }
            parseContainer(rotator, defaultValues);
        }
    }
}


async function registerListeners(name: string) {
    const container = document.querySelector('.main-container');
    if (container === null) {
        throw new Error('Missing main container');
    }
    
    let buttonsDefaultValues = {} as {[key: string]: string};
    let res = await fetch('/init?key='+name).then((res) => res.text());
    res.split('\n').forEach((button) => {
        console.log(button);
        const [id, value] = button.split('=');
        if (id == undefined || value == undefined) {
            throw new Error('Invalid button value');
        }
        buttonsDefaultValues[id] = value;
    });

    parseContainer(container, buttonsDefaultValues);
}

document.addEventListener('DOMContentLoaded', () => {
    let name = getName();
    registerListeners(name);
});