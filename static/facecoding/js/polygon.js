//This module was peiced togehter and adapted from a couple differnt
//sources online that I didn't document
//immidiately and unfortunately haven't been able to find
//by searching. None of the source docuements had any kind 
//of licencing attached to them.
//
//I am currently working from scratch on a replacement version of
//this written in d3.js, available here:
//  http://people.ucsc.edu/~jomicoll/d3/polygon.html
//
//The replacement will have the feature of
//smooth zooming to extreme magnification, which is important
//for a lot of applications in researh.



(function ($) {

    function isPointInPoly(poly, pt) {
        for (var c = false, i = -1, l = poly.length, j = l - 1; ++i < l; j = i)
            ((poly[i].y <= pt.y && pt.y < poly[j].y) || (poly[j].y <= pt.y && pt.y < poly[i].y))
            && (pt.x < (poly[j].x - poly[i].x) * (pt.y - poly[i].y) / (poly[j].y - poly[i].y) + poly[i].x)
            && (c = !c);

        return c;
    }


    $.fn.canvasAreaDraw = function (options, polys) {
        this.each(function (index, element) {
            init.apply(element, [index, element, options, polys]);
        });
    }
        
    var init = function (index, input, options, polys) {
        var currentId = 0;
        var polygons = polys || [[]];
        console.log(polys);

        var activePoint, settings;
        var $reset, $canvas, ctx, image;
        var draw, mousedown, stopdrag, move, resizeImg, resizeDepth, reset, rightclick, record;

        var oldMousePosX = 0;
        var oldMousePosY = 0;

        var disabled = $('#submitButton').attr('disabled') === 'disabled' ? true : false;

        settings = $.extend({
            imageUrl: $(this).attr('data-image-url')
        }, options);

        if ($(this).val().length) {
            polygons[currentId] = $(this).val().split(',').map(function (point) {
                return parseInt(point, 10);
            });
        } else {
            polygons[currentId] = [];
        }
        console.log(options);


        $reset = $('<button type="button" class="btn btn-danger"><i class="icon-trash"></i>Clear</button>');

        $canvas = $('<canvas>');

        ctx = $canvas[0].getContext('2d');
        console.log(ctx);
        var imageWidth = 0;
        var imageHeight = 512;
        var zoom = 1;

        image = new Image();
        depth = new Image();

        resizeDepth = function () {
            var aspect = image.width / image.height;
            imageWidth = 512 * aspect;
            imageHeight = 512;
            var width = 0;
            if (depth.height > 0)
                width += imageWidth;
            if (image.height > 0)
                width += imageWidth

            $canvas.attr('height', imageHeight).attr('width', width);
            $canvas.css('background-size', 'contain');

            draw();
        };

        resizeImg =  function () {
            zoom = image.height / imageHeight;
            resizeDepth();
        };


        $(depth).load(resizeDepth);
        $(image).load(resizeImg);

        image.src = settings.imageUrl;
        depth.src = settings.depthURL;

        $(document).ready(function () {
            console.log("entering .read(function () {");

            $(input).after($canvas, '<br>', $reset);

            $reset.click(reset);

            $canvas.on('mousedown', mousedown);
            $canvas.on('contextmenu', rightclick);
            $canvas.on('mouseup', stopdrag);
            setCurrentPolygon(1);
        });


        createNewPolygon = function () {
            console.log("creatng polygon");
            if (polygons[polygons.length - 1].length == 0) {
                currentId = polygons.length - 1;
            }
            else {
                currentId = polygons.length;
                polygons.push([]);
          }
            for (var i = 0; i < polygons.length; i++) {
                console.log(polygons[i]);
            }

            activePoint = 0;

            draw();
        }

        setCurrentPolygon = function (polygonID) {
            console.log("setting polygon");
            currentId = polygonID % polygons.length;
            if (currentId < 0)
                currentId = 0;

            draw();
        }

        reset = function () {
            polygons = [[]];
            currentId = 0;

            draw();
        };

        var vertexClickCount = 0;

        move = function (e) {
            if (disabled == true)
                return;

            if (!e.offsetX) {
                e.offsetX = (e.pageX - $(e.target).offset().left);
                e.offsetY = (e.pageY - $(e.target).offset().top);

            }

            if (e.offsetX > imageWidth)
                e.offsetX -= imageWidth;

            if( e.offsetX > 6 && e.offsetY > 6);
            vertexClickCount = 0;

            polygons[currentId][activePoint] = Math.round(e.offsetX);
            polygons[currentId][activePoint + 1] = Math.round(e.offsetY);

            record(currentId);
            draw();
        };

        stopdrag = function () {
            $(this).off('mousemove');

            if (vertexClickCount === 1) {
                createNewPolygon();
                return false;
            }

            record(currentId);
            activePoint = null;
        };

        rightclick = function (e) {
            if (false)
                return false;

            e.preventDefault();
            if (!e.offsetX) {
                e.offsetX = (e.pageX - $(e.target).offset().left);
                e.offsetY = (e.pageY - $(e.target).offset().top);

            }

            if (e.offsetX > imageWidth)
                e.offsetX -= imageWidth;

            var x = e.offsetX, y = e.offsetY;
            for (var i = 0; i < polygons[currentId].length; i += 2) {
                dis = Math.sqrt(Math.pow(x - polygons[currentId][i], 2) + Math.pow(y - polygons[currentId][i + 1], 2));
                if (dis < 6.0) {
                    polygons[currentId].splice(i, 2);

                    if (polygons[currentId].length == 0) {
                        for (var poly = currentId; poly < polygons.length - 1; ++poly)
                            polygons[poly] = polygons[poly + 1];
                        if (polygons.length > 1)
                        {
                            polygons.splice(polygons.length - 1);
                            currentId = polygons.length - 1;
                        }
                    }

                    draw();
                    record(currentId);
                    return false;
                }
            }

            var point = { x: e.offsetX, y: e.offsetY };
            for (var i = 0; i < polygons.length; ++i) {
                poly = [];
                for (var p = 0; p < polygons[i].length; p += 2)
                    poly.push({ x: polygons[i][p], y: polygons[i][p + 1] });

                if (isPointInPoly(poly, point)) {
                    setCurrentPolygon(i);
                    return false;
                }
            }


            return false;
        };

        mousedown = function (e) {
            if (disabled == true)
                return false;

            var x, y, dis, lineDis, insertAt = polygons[currentId].length;

            if (e.which === 3) {
                return false;
            }

            e.preventDefault();
            if (!e.offsetX) {
                e.offsetX = (e.pageX - $(e.target).offset().left);
                e.offsetY = (e.pageY - $(e.target).offset().top);
            }

            if (e.offsetX > imageWidth)
                e.offsetX -= imageWidth;

            x = e.offsetX; y = e.offsetY;


            for (var i = 0; i < polygons[currentId].length; i += 2) {
                dis = Math.sqrt(Math.pow(x - polygons[currentId][i], 2) + Math.pow(y - polygons[currentId][i + 1], 2));
                if (dis < 6) {
                    vertexClickCount += 1;

                    activePoint = i;
                    oldMousePosX = x;
                    oldMousePosY = y;
                    $(this).on('mousemove', move);

                    return false;
                }
            }
            if (true)  {//modify later.
                vertexClickCount = 0;
    
                for (var i = 0; i < polygons[currentId].length; i += 2) {
                    if (i > 1) {
                        lineDis = dotLineLength(
                          x, y,
                          polygons[currentId][i], polygons[currentId][i + 1],
                          polygons[currentId][i - 2], polygons[currentId][i - 1],
                          true
                        );
                        if (lineDis < 6) {
                            insertAt = i;
                        }
                    }
                }
    
                polygons[currentId].splice(insertAt, 0, Math.round(x), Math.round(y));
                activePoint = insertAt;
                oldMousePosX = x;
                oldMousePosY = y;
                $(this).on('mousemove', move);
            };
            draw();
            record(currentId);

            return false;
        };

        draw = function () {

            ctx.canvas.width = ctx.canvas.width;

            var imgs = [image];
            if (depth.width != 0)
                imgs.push(depth);

            for (var imgIndx = 0; imgIndx < imgs.length; imgIndx++) {
                var offsetByX = imgIndx * imageWidth;
                for (var polyId = 0; polyId < polygons.length; ++polyId) {
                    record(polyId);

                    if (polygons[polyId].length < 2) {
                        continue;
                    }

                    ctx.globalCompositeOperation = 'destination-over';
                    ctx.fillStyle = polyId == currentId ? 'rgb(255,255,255)' : 'rgba(255,255,255,0.50)';
                    ctx.strokeStyle = polyId == currentId ? 'rgb(255,  0, 20)' : 'rgb(20,0,255)';
                    ctx.lineWidth = polyId == currentId ? 2 : 1;

                    ctx.beginPath();
                    ctx.font="15px Verdana";
                    ctx.moveTo(polygons[polyId][0] + offsetByX, polygons[polyId][1]);
                    for (var i = 0; i < polygons[polyId].length; i += 2) {
                        ctx.fillRect(polygons[polyId][i] + offsetByX - 2, polygons[polyId][i + 1] - 2, 4, 4);
                        ctx.fillText(''+(i/2), polygons[polyId][i] + offsetByX -2, polygons[polyId][i+1]-2);
                        ctx.strokeRect(polygons[polyId][i] + offsetByX - 2, polygons[polyId][i + 1] - 2, 4, 4);
                        if (polygons[polyId].length > 2 && i > 1) {
                            ctx.lineTo(polygons[polyId][i] + offsetByX, polygons[polyId][i + 1]);
                        }
                    }
                    ctx.closePath();
                    ctx.fillStyle = polyId == currentId ? 'rgba(0,255,0,0.3)' : 'rgba(0, 200,255,0.25)';
                    //ctx.fill();
                    ctx.stroke();
                }
            }

            ctx.drawImage(image, 0, 0, imageWidth, imageHeight);
            if (depth.height > 0)
                ctx.drawImage(depth, imageWidth, 0, imageWidth, imageHeight);
        };

        record = function (poly) {

            var round = Math.round;

            var newPolygons = [];

            for (var i = 0; i < polygons.length; i++) {
                var oldPoly = polygons[i];
                var newPoly = [];
                for (var j = 0; j < oldPoly.length; j++) {
                    newPoly.push(round(oldPoly[j] * zoom))
                }

                newPolygons.push(newPoly);
            }

            $('#polygons_verticies').val(JSON.stringify(polygons));
        };

        $(input).on('change', function () {
            if ($(this).val().length) {
                polygons[currentId] = $(this).val().split(',').map(function (point) {
                    return Math.round(parseInt(point, 10) / zoom);
                });
            } else {
                polygons[currentId] = [];
            }
            draw();
        });

    };

    $(document).ready(function () {
        $('.canvas-area[data-image-url]').canvasAreaDraw();
    });

    var dotLineLength = function (x, y, x0, y0, x1, y1, o) {
        function lineLength(x, y, x0, y0) {
            return Math.sqrt((x -= x0) * x + (y -= y0) * y);
        }
        if (o && !(o = function (x, y, x0, y0, x1, y1) {
          if (!(x1 - x0)) return { x: x0, y: y };
        else if (!(y1 - y0)) return { x: x, y: y0 };
          var left, tg = -1 / ((y1 - y0) / (x1 - x0));
          return { x: left = (x1 * (x * tg - y + y0) + x0 * (x * -tg + y - y1)) / (tg * (x1 - x0) + y0 - y1), y: tg * left - tg * x + y };
        }(x, y, x0, y0, x1, y1), o.x >= Math.min(x0, x1) && o.x <= Math.max(x0, x1) && o.y >= Math.min(y0, y1) && o.y <= Math.max(y0, y1))) {
            var l1 = lineLength(x, y, x0, y0), l2 = lineLength(x, y, x1, y1);
            return l1 > l2 ? l2 : l1;
        }
        else {
            var a = y0 - y1, b = x1 - x0, c = x0 * y1 - y0 * x1;
            return Math.abs(a * x + b * y + c) / Math.sqrt(a * a + b * b);
        }
    };
})(jQuery);
