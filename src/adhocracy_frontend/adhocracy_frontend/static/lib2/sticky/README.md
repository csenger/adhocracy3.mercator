# Sticky.js

## Use [the better script](https://github.com/wilddeer/stickyfill)

Makes elements sticky*.

Supports all features of [sticky-kit.js](https://github.com/leafo/sticky-kit) and [sticky.js](https://github.com/garand/sticky), and
implements extra features:

* Sticky modes: _stacked_ / _mutually exclusive_.
* Any restricting containers possible, not only parent ones (unlike [sticky-kit.js](https://github.com/leafo/sticky-kit)).
* No jquery dependency. Works regardless of jquery presence, but if it is, injects jquery plugin.
* Careful treatment of element's style, like absolute/relative position, floating etc.
* Works correctly on resizing.
* Minds paddings/margins.
* Multiple stacking
* Dynamically hide/show/remove/append elements

*Sticky elements — ones become fixed being scrolled on.

## Use

```js
//jQuery way
$(".sticky-element").sticky({/*options*/});

//no-jQuery way
var sticky = new Sticky(document.querySelector(".sticky-element"), {/* options */});
```

## Options

```js
{
    //How much pixels to mind from the top
    offset: 0,

    //Any element, element selector or bounding box like {top: 0, bottom: 100 } or { top: element, bottom: element }
    restrictWithin: parent,

    //TODO: which boundary to bound to
    vAlign: 'top',

    //Class to add when element is sticked
    stickyClass: "is-stuck",

    //Class to add to a spacer (placeholder when element is stuck)
    stubClass: "sticky-stub",

    //When element is parked bottom
    bottomClass: "is-bottom",

    //When element is parked on top
    topClass: "is-top",

    //Name of a group to stack elements within. _undefined_ stack won’t relate element to any group
    stack: null
}
```

## API

#### `recalc` — forces update position, sizes, sticking. Automatically called on window resizes.
```js
//jQuery way
$(document).trigger("sticky:recalc");

//no-jQuery way
document.dispatchEvent(new CustomEvent("sticky:recalc"));
```

You can target recalc by calling it on sticky element itself:
```js
$(".sticky-element").trigger("sticky:recalc")
```

#### `disable` — unhooks sticky controller from element. Called automatically when element is removed. Useful if you hide element.
```js
element.attr("hidden", true);
element.trigger("sticky:disable");
```

#### `enable` — enables previously disabled sticky element. Useful when you show elemens.
```js
element.removeAttr("hidden");
element.trigger("sticky:enable");
```

Beware that not every browser supports `dispatchEvent` method. In order to make IE < 10 work, use one of the polyfills: [polyfill combinator](https://github.com/jonathantneal/polyfill), [modernizr](https://github.com/Modernizr/Modernizr) or [ES5 shim](https://github.com/termi/ES5-DOM-SHIM).