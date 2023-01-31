// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = Stripe('pk_test_51MUAERKZ8ITmwoDIcpcujDz4LbtTTESUeC1O1Lw6RvVIQWIbF0yD0yrtlcEJNQXwgN7RcWHExDxSMjcbDWGw1Pit0011EnxEx9');

document.querySelector("#payment-form").addEventListener("submit", handleSubmit);
const appearance = {
    theme: 'stripe',

    variables: {
        colorPrimary: '#5b2ea1',
        colorBackground: '#ffffff',
        colorText: '#30313d',
        colorDanger: '#df1b41',
        fontFamily: 'Archivo, Ideal Sans, system-ui, sans-serif',
        spacingUnit: '4px',
        borderRadius: '4px',
    },

    rules: {
        '.Tab': {
            boxShadow: '0px 2px 2px 0px rgba(0, 0, 0, 0.25)',
        },
        '.Tab:hover': {
            transitionDuration: '0.25s',
            boxShadow: '0px 2px 1px 0px rgba(0, 0, 0, 0.15)',
        },
    }
};
const options = {
    fonts: [{
        cssSrc: 'https://fonts.googleapis.com/css2?family=Archivo&display=swap'
    }],
    clientSecret: c_secret,
    appearance: appearance,
    // Fully customizable with appearance API.
};

// Set up Stripe.js and Elements to use in checkout form, passing the client secret obtained in step 3
const elements = stripe.elements(options);

console.log(c_secret)
// Create and mount the Payment Element
const paymentElement = elements.create("payment")
paymentElement.mount("#payment-element")
var url = location.protocol + '//' + location.host

async function handleSubmit(e) {
    e.preventDefault();
    let submit = document.getElementById("submit")
    let address = document.getElementById("delivery")
    submit.disabled = true
    submit.value = "Please Wait..."
    const {error} = await stripe.confirmPayment({
        elements,
        confirmParams: {
            // Make sure to change this to your payment completion page
            return_url: url + "/checkout/confirm/" + address.value,
            receipt_email: emailAddress,
        },
    });

    // This point will only be reached if there is an immediate error when
    // confirming the payment. Otherwise, your customer will be redirected to
    // your `return_url`. For some payment methods like iDEAL, your customer will
    // be redirected to an intermediate site first to authorize the payment, then
    // redirected to the `return_url`.
    submit.disabled = false
    submit.value = "Pay with Stripe"
    if (error.type === "card_error" || error.type === "validation_error") {
        showMessage(error.message);
    } else {
        showMessage("An unexpected error occurred.");
    }
}

function showMessage(messageText) {
    const messageContainer = document.querySelector("#error-message");

    messageContainer.classList.remove("d-none");
    messageContainer.textContent = messageText;

    setTimeout(function () {
        messageContainer.classList.add("d-none");
        messageText.textContent = "";
    }, 4000);
}