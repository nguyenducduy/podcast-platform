import Vue from "vue";

export const bus = new Vue();

export function getBase64(img, callback) {
  const reader = new FileReader();
  reader.addEventListener("load", () => callback(reader.result));
  reader.readAsDataURL(img);
}

export function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export function randomID() {
  return (
    "_" +
    Math.random()
      .toString(36)
      .substr(2, 9)
  );
}

export function getVariables(pagination, curPage) {
  let variables: any = {};
  const totalPages: number = pagination.total / pagination.pageSize;
  const currentPage: number = parseInt(curPage);

  variables["first"] = pagination.pageSize * currentPage;

  if (totalPages === 0) {
    variables["last"] = pagination.pageSize;
  } else {
    variables["last"] =
      currentPage > totalPages
        ? pagination.total % pagination.pageSize
        : pagination.pageSize;
  }

  return variables;
}
