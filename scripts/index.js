(function() {
    var donation = {
        type: "monthly",
        amount: 1000, // cents
        project: null,
        comment: null
    };

    function selectAmount(e) {
        e.preventDefault();
        document.querySelector(".amounts .active").classList.remove("active");
        e.target.classList.add("active");
        var custom = document.querySelector("#custom-amount");
        var amount = e.target.dataset.amount;
        if (amount === "custom") {
            custom.classList.remove("hidden");
            donation.amount = +document.querySelector("#custom-amount-text").value * 100;
        } else {
            custom.classList.add("hidden");
            donation.amount = +e.target.dataset.amount * 100;
        }
    }

    function selectFrequency(e) {
        e.preventDefault();
        document.querySelector(".frequencies .active").classList.remove("active");
        e.target.classList.add("active");
        donation.type = e.target.dataset.frequency;
    }

    var amounts = document.querySelectorAll(".amounts button");
    for (var i = 0; i < amounts.length; i++) {
        amounts[i].addEventListener("click", selectAmount);
    }

    var frequencies = document.querySelectorAll(".frequencies button");
    for (var i = 0; i < frequencies.length; i++) {
        frequencies[i].addEventListener("click", selectFrequency);
    }

    document.getElementById("custom-amount-text").addEventListener("change", function(e) {
        var value = +e.target.value;
        if (isNaN(value)) {
            value = 1;
        }
        e.target.value = value;
        donation.amount = value * 100;
    });

    var project = document.getElementById("project")
    if (project) {
        project.addEventListener("change", function(e) {
            if (e.target.value === "null") {
                donation.project = null;
            } else {
                donation.project = e.target.value;
            }
        });
    }

    document.getElementById("donate-button").addEventListener("click", function(e) {
        e.preventDefault();
        if (e.target.getAttribute("disabled")) {
            return;
        }

        var handler = StripeCheckout.configure({
            name: your_name,
            key: window.stripe_key,
            image: window.avatar,
            locale: 'auto',
            description: donation.type == "monthly" ? "Monthly Donation" : "One-time Donation",
            panelLabel: "Donate {{amount}}",
            amount: donation.amount,
            bitcoin: donation.type == "once" && window.bitcoin,
            token: function(token) {
                e.target.setAttribute("disabled", "");
                e.target.textContent = "Submitting...";

                var data = new FormData();
                data.append("stripe_token", token.id);
                data.append("email", token.email);
                data.append("amount", donation.amount);
                data.append("type", donation.type);
                data.append("comment", donation.comment);
                if (donation.project !== null) {
                    data.append("project", donation.project);
                }
                var xhr = new XMLHttpRequest();
                xhr.open("POST", "donate");
                xhr.onload = function() {
                    document.getElementById("donation-stuff").classList.add("hidden");
                    document.getElementById("thanks").classList.remove("hidden");
                    var res = JSON.parse(this.responseText);
                    if (res.newAccount) {
                        document.getElementById("new-donor-password").classList.remove("hidden");
                    }
                };
                xhr.send(data);
            }
        });

        handler.open();
    });
})();
