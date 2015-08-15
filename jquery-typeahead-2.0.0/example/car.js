$('#car_v1-query').typeahead({
minLength: 1,
order: "asc",
offset: true,
hint: true,
source: {
    car: {
        data: ["My first added brand", "M1 added brand at start"],
        url: {
            type: "POST",
            url: "car_v1.json",
            data: {
                myKey: "myValue"
            }
        }
    }
},
callback: {
    onClick: function (node, a, item, event) {

        console.log(node)
        console.log(a)
        console.log(item)
        console.log(event)

        console.log('onClick function triggered');

    },
    onSubmit: function (node, form, item, event) {

        console.log(node)
        console.log(form)
        console.log(item)
        console.log(event)

        console.log('onSubmit override function triggered');

    }
}
});
