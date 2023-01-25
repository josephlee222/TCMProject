// Set your publishable key: remember to change this to your live publishable key in production
// See your keys here: https://dashboard.stripe.com/apikeys
const stripe = Stripe('pk_test_51MUAERKZ8ITmwoDIcpcujDz4LbtTTESUeC1O1Lw6RvVIQWIbF0yD0yrtlcEJNQXwgN7RcWHExDxSMjcbDWGw1Pit0011EnxEx9');

document.querySelector("#payment-form").addEventListener("submit", handleSubmit);

const options = {
    fonts: [{
        family: 'Archivo',
        src: 'url(https://fonts.googleapis.com/css2?family=Archivo:wght@300;400;500;700&display=swap)',
        weight: '500',
    }],
    clientSecret: c_secret,
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

    const {error} = await stripe.confirmPayment({
        elements,
        confirmParams: {
            // Make sure to change this to your payment completion page
            return_url: url + "/checkout/confirm/0",
            receipt_email: emailAddress,
        },
    });

    // This point will only be reached if there is an immediate error when
    // confirming the payment. Otherwise, your customer will be redirected to
    // your `return_url`. For some payment methods like iDEAL, your customer will
    // be redirected to an intermediate site first to authorize the payment, then
    // redirected to the `return_url`.
    if (error.type === "card_error" || error.type === "validation_error") {
        showMessage(error.message);
    } else {
        showMessage("An unexpected error occurred.");
    }
}

function showMessage(messageText) {
    const messageContainer = document.querySelector("#payment-message");

    messageContainer.classList.remove("hidden");
    messageContainer.textContent = messageText;

    setTimeout(function () {
        messageContainer.classList.add("hidden");
        messageText.textContent = "";
    }, 4000);
}