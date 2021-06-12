$(document).ready(function () {
  // get all list items here
  $("#data_form").submit(handleFormSubmit);

  $.ajax({
    method: "get",
    url: "http://localhost:8000/get_categorical",
    contentType: "application/json",
    success: (data) => {
      addListItems(data);
      $("#loader").addClass("hidden");
    },
    error: (_1, _2, error) => {
      console.log({ error });
      $("#loader").addClass("hidden");
    },
    beforeSend: () => $("#loader").removeClass("hidden"),
  });
});

function addListItems(data) {
  data.districts.forEach((val) => {
    $("#select_district").append(
      new Option(val.substr(0, 1) + val.toLowerCase().substr(1), val)
    );
  });

  data.crops.forEach((val) => {
    $("#select_crop").append(
      new Option(val.substr(0, 1) + val.toLowerCase().substr(1), val)
    );
  });

  data.soils.forEach((val) => {
    $("#select_soil").append(
      new Option(val.substr(0, 1) + val.toLowerCase().substr(1), val)
    );
  });
}

function handleFormSubmit(event) {
  event.preventDefault();
  $("#info_box").removeClass("py-1 bg-red-400 bg-green-400");
  $("#info_box").text("");

  const payload = {
    city: $("#select_district").val(),
    crop: $("#select_crop").val(),
    soil: $("#select_soil").val(),
    area: $("#text_area").val(),
  };

  if (!payload.area || !payload.crop || !payload.city || !payload.soil) {
    $("#info_box").removeClass("bg-green-400");
    $("#info_box").addClass("py-1 bg-red-400");
    $("#info_box").text("Please fill all the information correctly.");
    return;
  }

  let season = "Season:_";
  let month = new Date().getMonth();
  if (month >= 7 && month <= 10) month += "Kharif";
  else season += "Rabi";

  var settings = {
    url: "http://localhost:8000/get_yield",
    method: "POST",
    timeout: 0,
    headers: {
      "Content-Type": "application/json",
    },
    data: JSON.stringify({
      ...payload,
      season: "Rabi",
    }),
    success: (data) => {
      console.log({ yield: data });
      $("#info_box").removeClass("bg-red-400");
      $("#info_box").addClass("py-1 bg-green-400");
      $("#info_box").html(
        `Expected harvest will be <b>${data.produce} tons.</b>`
      );
      $("#loader").addClass("hidden");
    },
    error: (_1, _2, error) => {
      console.log({ error });
      $("#info_box").removeClass("bg-green-400");
      $("#info_box").addClass("py-1 bg-red-400");
      $("#info_box").text("Something went wrong. Please try again later.");
      $("#loader").addClass("hidden");
    },
    beforeSend: () => $("#loader").removeClass("hidden"),
  };

  $.ajax(settings);
}
